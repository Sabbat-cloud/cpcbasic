import pygame
import numpy as np


class SoundEngine:
    def __init__(self, sample_rate=44100):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=sample_rate, size=-16, channels=2, buffer=1024)
            except Exception:
                pass

        self.sample_rate = sample_rate
        # Interrupción del firmware del CPC (300Hz; el motor de sonido divide entre 3 -> 100Hz / centisegundos)
        self.cpc_int_freq = 300.0
        self.samples_per_tick = int(self.sample_rate / self.cpc_int_freq)

        # LUT logarítmica exacta del DAC del AY-3-8912 (16 niveles -> 16-bit signed)
        self.AY_VOL_LUT = np.array([
            0, 235, 335, 474, 679, 959, 1373, 1944,
            2783, 3965, 5606, 7949, 11283, 15998, 22699, 32767
        ], dtype=np.int16)

        # Precalcular tabla de las 16 formas de envolvente hardware del AY-3-8912 (Reg 13, shapes 0..15)
        self._hw_env_lut = self._build_hw_env_lut()

        # Precalcular secuencia del LFSR de 17 bits del AY-3-8912 (x^17 + x^14 + 1, 131071 estados)
        self._lfsr_table = self._build_lfsr_table(131072)
        self._lfsr_pos = 0

        # Fase continua por canal para evitar clics entre notas consecutivas
        self._channel_phase = {0: 0.0, 1: 0.0, 2: 0.0}

        # Estado de registros del AY-3-8912 (0..15)
        self.psg_registers = [0] * 16
        self.psg_registers[7] = 0x3F  # Mixer: todos los canales desactivados inicialmente

        self.envelopes_vol = {}
        self.envelopes_tone = {}
        self.reset()

    def _build_hw_env_lut(self):
        """Construye una tabla 16x48 con los niveles (0..15) de cada shape (0..15) del AY-3-8912.
        Pasos 0..15: ciclo inicial (cycle 0).
        Pasos 16..47: ciclos posteriores (cycle >= 1, periódico cada 32 pasos para todas las formas).
        """
        lut = np.zeros((16, 48), dtype=np.int32)
        for shape in range(16):
            cont = (shape >> 3) & 1
            att = (shape >> 2) & 1
            alt = (shape >> 1) & 1
            hold = shape & 1

            # Ciclo 0 (pasos 0..15)
            for s in range(16):
                lut[shape, s] = s if att else (15 - s)

            # Ciclos >= 1 (pasos 16..47)
            for idx in range(16, 48):
                cycle = idx // 16  # 1 o 2
                s = idx % 16
                if not cont:
                    lut[shape, idx] = 0
                elif hold:
                    lut[shape, idx] = 15 if (att ^ alt) else 0
                else:
                    dir_up = (att ^ (cycle & 1)) if alt else att
                    lut[shape, idx] = s if dir_up else (15 - s)
        return lut

    def _build_lfsr_table(self, length=131072):
        """Genera la secuencia exacta del LFSR de 17 bits del AY-3-8912 (polinomio bit0 ^ bit3)."""
        table = np.empty(length, dtype=np.int32)
        lfsr = 1
        for i in range(length):
            table[i] = lfsr & 1
            bit = (lfsr ^ (lfsr >> 3)) & 1
            lfsr = (lfsr >> 1) | (bit << 16)
        return table

    def reset(self):
        """SOUND RESET (&BCA7): Limpia colas, estados de canales y silencia el PSG."""
        self.channel_queues = {0: [], 1: [], 2: []}
        # Estado del canal equivalente a (ix+$03) en sound.asm:
        # 0 = inactivo, 1..7 = máscara rendezvous, 8 = held (Hold), 16 = reproduciendo
        self.channel_status_byte = {0: 0, 1: 0, 2: 0}
        self.channel_held = {0: False, 1: False, 2: False}
        self.global_held = False
        self.sq_events_armed = {0: False, 1: False, 2: False}
        self.sq_events_pending = {0: False, 1: False, 2: False}
        self.psg_registers[7] = 0x3F
        for r in (8, 9, 10):
            self.psg_registers[r] = 0

        if pygame.mixer.get_init():
            if pygame.mixer.get_num_channels() < 3:
                pygame.mixer.set_num_channels(3)
            for c_id in range(3):
                try:
                    pygame.mixer.Channel(c_id).stop()
                except Exception:
                    pass

    def set_env(self, env_no, sections):
        """Define una envolvente de volumen ENV (1..15), hasta 5 secciones."""
        if not (1 <= env_no <= 15):
            return False
        grouped = []
        for i in range(0, min(len(sections), 15), 3):
            chunk = list(sections[i:i + 3])
            if len(chunk) < 3:
                break
            grouped.append(chunk)
        self.envelopes_vol[env_no] = grouped
        return True

    def set_ent(self, ent_no, sections):
        """Define una envolvente de tono ENT (1..15 o -1..-15 repetitiva), hasta 5 secciones."""
        if ent_no == 0 or abs(ent_no) > 15:
            return False
        repeat = (ent_no < 0)
        actual_no = abs(ent_no)
        grouped = []
        for i in range(0, min(len(sections), 15), 3):
            chunk = list(sections[i:i + 3])
            if len(chunk) < 3:
                break
            grouped.append(chunk)
        self.envelopes_tone[actual_no] = {
            'sections': grouped,
            'repeat': repeat
        }
        return True

    def set_env_from_ram(self, env_no, block_bytes):
        """SOUND AMPL ENVELOPE (&BCBC): Define ENV desde bloque de memoria de 16 bytes."""
        if not (1 <= env_no <= 15) or not block_bytes:
            return False
        num_sec = min(5, block_bytes[0] & 0x7F)
        grouped = []
        for i in range(num_sec):
            base = 1 + i * 3
            if base + 2 >= len(block_bytes):
                break
            b0 = block_bytes[base]
            b1 = block_bytes[base + 1]
            b2 = block_bytes[base + 2]
            if b0 & 0x80:
                # Hardware envelope: b0 = 0x80 | shape, b1 = period_low, b2 = period_high
                shape = b0 & 0x0F
                hw_period = b1 | (b2 << 8)
                grouped.append([-1, shape, hw_period])
            else:
                step_count = b0 & 0x7F
                step_size = (b1 - 256) if (b1 >= 128 and step_count > 0) else b1
                grouped.append([step_count, step_size, b2])
        self.envelopes_vol[env_no] = grouped
        return True

    def set_ent_from_ram(self, ent_no, block_bytes):
        """SOUND TONE ENVELOPE (&BCBF): Define ENT desde bloque de memoria de 16 bytes."""
        if not (1 <= ent_no <= 15) or not block_bytes:
            return False
        repeat = bool(block_bytes[0] & 0x80)
        num_sec = min(5, block_bytes[0] & 0x7F)
        grouped = []
        for i in range(num_sec):
            base = 1 + i * 3
            if base + 2 >= len(block_bytes):
                break
            b0 = block_bytes[base]
            b1 = block_bytes[base + 1]
            b2 = block_bytes[base + 2]
            if b0 >= 0xF0:
                # Periodo absoluto: b0 = 0xF0 + high_nibble, b1 = low_byte, b2 = pause
                abs_period = ((b0 - 0xF0) << 8) | b1
                grouped.append([-1, abs_period, b2])
            else:
                step_count = b0
                step_size = (b1 - 256) if b1 >= 128 else b1
                grouped.append([step_count, step_size, b2])
        self.envelopes_tone[ent_no] = {
            'sections': grouped,
            'repeat': repeat
        }
        return True

    def _simulate_volume_envelope(self, duration, volume, env):
        """Simula exactamente update_volume_envelope de sound.asm (líneas 761-958).
        Devuelve (total_ticks, tick_vols, hw_segments).
        Cada elemento de hw_segments es (start_tick, end_tick, trigger_tick, shape, hw_period).
        """
        default_sections = [[1, 0, 0]]
        env_sections = self.envelopes_vol.get(env) if (env > 0 and self.envelopes_vol.get(env)) else None
        curr_sections = env_sections if env_sections else default_sections

        dur = -1 if duration == 0 else int(duration)
        vol_reg = (int(volume) & 0x0F) | 0x80  # Bit 7 indica volumen inicial aún no escrito

        sec_idx = 0
        e = curr_sections[0][0]

        # Segmentos acumulados en centisegundos: (csec, vol_reg, hw_trigger_csec, hw_shape, hw_period)
        csec_segments = []
        total_csec = 0
        hw_shape = 0
        hw_period = 1
        hw_trigger_csec = 0

        max_csec = 30000  # Límite de seguridad (5 minutos)

        while total_csec < max_csec:
            # Procesar secciones de envolvente hardware (-1, shape, period)
            hw_loop_guard = 0
            while e == -1 and hw_loop_guard < 16:
                hw_loop_guard += 1
                _, shape_val, period_val = curr_sections[sec_idx]
                hw_shape = int(shape_val) & 0x0F
                hw_period = int(period_val) & 0xFFFF
                hw_trigger_csec = total_csec
                vol_reg = 0x10  # Modo envolvente hardware (bit 4 = 1, bit 7 = 0)

                # unknown_sound_function: avanzar a la siguiente sección
                sec_idx += 1
                if sec_idx >= len(curr_sections):
                    if dur >= 0:
                        curr_sections = default_sections
                        sec_idx = 0
                    else:
                        dur += 1
                        if dur == 0:
                            # sound.asm líneas 908-914: si la envolvente termina en sección HW,
                            # carga default_volume_envelope (1, 0, 200) para que suene
                            curr_sections = default_sections
                            sec_idx = 0
                        else:
                            sec_idx = 0
                e = curr_sections[sec_idx][0]

            steps, step_size, pause_time = curr_sections[sec_idx]
            steps = int(steps)
            step_size = int(step_size)
            pause_time = int(pause_time) & 0xFF

            if steps == 0:
                # Sección de volumen absoluto (0, abs_vol, pause_time) -> sound.asm línea 881
                vol_reg = step_size & 0x0F
                e = 0
            else:
                # Sección de volumen relativo (steps > 0, step_size, pause_time) -> sound.asm líneas 847-851
                e -= 1
                if step_size != 0 or (vol_reg & 0x80) != 0:
                    # En sound.asm línea 848 (add a,c : and $0f) y manual pág. 352: envolvente circular módulo 16
                    vol_reg = ((vol_reg & 0x0F) + step_size) & 0x0F
                # Si step_size == 0 y bit 7 == 0 (ej. tras envolvente hardware 0x10), conserva vol_reg

            pause_csec = 256 if pause_time == 0 else pause_time

            terminate = False
            if dur > 0:
                if dur <= pause_csec:
                    step_csec = dur
                    dur = 0
                    terminate = True
                else:
                    step_csec = pause_csec
                    dur -= pause_csec
            else:
                step_csec = pause_csec

            if step_csec > 0:
                csec_segments.append((step_csec, vol_reg, hw_trigger_csec, hw_shape, hw_period))
                total_csec += step_csec

            if terminate:
                break

            if e <= 0:
                # Avanzar a la siguiente sección (unknown_sound_function)
                sec_idx += 1
                if sec_idx >= len(curr_sections):
                    if dur > 0:
                        curr_sections = default_sections
                        sec_idx = 0
                    else:
                        dur += 1
                        if dur >= 0:
                            break
                        sec_idx = 0
                e = curr_sections[sec_idx][0]

        total_ticks = total_csec * 3
        if total_ticks <= 0:
            return 0, np.zeros(0, dtype=np.int32), []

        tick_vols = np.zeros(total_ticks, dtype=np.int32)
        hw_segments = []
        t_idx = 0
        for step_csec, v_reg, trig_csec, h_shape, h_per in csec_segments:
            ticks = step_csec * 3
            end_t = min(t_idx + ticks, total_ticks)
            if v_reg == 0x10:
                hw_segments.append((t_idx, end_t, trig_csec * 3, h_shape, h_per))
            else:
                tick_vols[t_idx:end_t] = v_reg & 0x0F
            t_idx = end_t

        return total_ticks, tick_vols, hw_segments

    def _simulate_tone_envelope(self, total_ticks, period, ent):
        """Simula exactamente tone_envelope_function de sound.asm (líneas 1013-1114)."""
        current_period = int(period) & 0x0FFF
        tick_periods = np.full(total_ticks, current_period, dtype=np.float64)

        ent_idx = abs(int(ent))
        if ent_idx == 0 or ent_idx not in self.envelopes_tone:
            return tick_periods

        ent_data = self.envelopes_tone[ent_idx]
        if isinstance(ent_data, dict):
            sections = ent_data.get('sections', [])
            repeat = ent_data.get('repeat', False)
        else:
            sections = ent_data
            repeat = (ent < 0)

        if not sections:
            return tick_periods

        t_idx = 0
        while t_idx < total_ticks:
            for section in sections:
                if t_idx >= total_ticks:
                    break
                steps, step_size, pause_time = section
                steps = int(steps)
                step_size = int(step_size)
                pause_time = int(pause_time) & 0xFF
                pause_csec = 256 if pause_time == 0 else pause_time
                ticks_per_step = pause_csec * 3

                if steps == -1:
                    # Periodo absoluto (=period, pause_time)
                    current_period = step_size & 0x0FFF
                    end_t = min(t_idx + ticks_per_step, total_ticks)
                    tick_periods[t_idx:end_t] = current_period
                    t_idx = end_t
                else:
                    # sound.asm líneas 1108-1113: si steps == 0 en ENT, cuenta como 1 paso relativo
                    actual_steps = max(1, steps)
                    for _ in range(actual_steps):
                        if t_idx >= total_ticks:
                            break
                        current_period = (current_period + step_size) & 0x0FFF
                        end_t = min(t_idx + ticks_per_step, total_ticks)
                        tick_periods[t_idx:end_t] = current_period
                        t_idx = end_t

            if not repeat:
                if t_idx < total_ticks:
                    tick_periods[t_idx:] = current_period
                break

        return tick_periods

    def _synthesize_sound(self, c_id, period, duration, volume, env=0, ent=0, noise=0):
        """Sintetiza el buffer de audio de un sonido para el canal indicado."""
        total_ticks, tick_vols, hw_segments = self._simulate_volume_envelope(duration, volume, env)
        if total_ticks <= 0:
            return None

        tick_periods = self._simulate_tone_envelope(total_ticks, period, ent)
        num_samples = total_ticks * self.samples_per_tick

        # 1. Expandir volúmenes a resolución de sample
        expanded_vols = np.repeat(tick_vols, self.samples_per_tick)

        # Aplicar segmentos de envolvente hardware del AY-3-8912 a resolución de sample
        # En el AY-3-8912 cada paso de los 16 niveles dura 16 * EP ciclos de reloj (1MHz / 16 = 62500 Hz)
        for start_t, end_t, trig_t, h_shape, h_per in hw_segments:
            s_start = start_t * self.samples_per_tick
            s_end = min(end_t * self.samples_per_tick, num_samples)
            s_trig = trig_t * self.samples_per_tick
            if s_end > s_start:
                ep = max(1, h_per)
                step_rate = 62500.0 / (ep * self.sample_rate)
                n_idx = np.arange(s_start - s_trig, s_end - s_trig, dtype=np.float64)
                steps_elapsed = (n_idx * step_rate).astype(np.int32)
                lut_idx = np.where(steps_elapsed < 16, steps_elapsed, 16 + ((steps_elapsed - 16) & 31))
                expanded_vols[s_start:s_end] = self._hw_env_lut[h_shape & 0x0F, lut_idx]

        expanded_vols = np.clip(expanded_vols, 0, 15)
        amplitudes = self.AY_VOL_LUT[expanded_vols]

        # 2. Expandir periodos y generar onda cuadrada de tono con fase continua
        expanded_periods = np.repeat(tick_periods, self.samples_per_tick)
        # En sound.asm líneas 629-643: si period != 0 o ent != 0, se activa set_tone_and_get_tone_envelope
        ent_idx = abs(int(ent))
        tone_enabled = (period > 0) or (ent_idx > 0)
        noise_enabled = (noise > 0)

        # Actualizar espejo de registros del AY-3-8912
        self.psg_registers[c_id * 2] = int(period) & 0xFF
        self.psg_registers[c_id * 2 + 1] = (int(period) >> 8) & 0x0F
        if noise_enabled:
            self.psg_registers[6] = int(noise) & 0x1F
        self.psg_registers[8 + c_id] = int(volume) & 0x0F
        if tone_enabled:
            self.psg_registers[7] &= ~(1 << c_id)
        else:
            self.psg_registers[7] |= (1 << c_id)
        if noise_enabled:
            self.psg_registers[7] &= ~(1 << (c_id + 3))
        else:
            self.psg_registers[7] |= (1 << (c_id + 3))

        # En sound.asm líneas 996-1004: si ni tono ni ruido están activos, el canal se silencia
        if not tone_enabled and not noise_enabled:
            amplitudes = np.zeros(num_samples, dtype=np.int16)
            tone_wave = np.ones(num_samples, dtype=np.int32)
        elif tone_enabled:
            freqs = np.divide(
                62500.0,
                expanded_periods,
                out=np.zeros_like(expanded_periods),
                where=expanded_periods > 0
            )
            start_phase = self._channel_phase.get(c_id, 0.0)
            phase_inc = freqs * (2.0 * np.pi / self.sample_rate)
            phase = start_phase + np.cumsum(phase_inc)
            if len(phase) > 0:
                self._channel_phase[c_id] = float(phase[-1] % (2.0 * np.pi))
            tone_wave = (np.sin(phase) >= 0).astype(np.int32)
            # Donde el periodo instantáneo es 0, la puerta de tono queda en 1
            if np.any(expanded_periods <= 0):
                tone_wave = np.where(expanded_periods <= 0, 1, tone_wave)
        else:
            tone_wave = np.ones(num_samples, dtype=np.int32)

        # 3. Generador de ruido LFSR de 17 bits del AY-3-8912 (F_noise = 62500 / noise)
        if noise_enabled:
            noise_val = max(1, int(noise) & 0x1F)
            noise_freq = 62500.0 / noise_val
            step_inc = noise_freq / self.sample_rate
            lfsr_mask = len(self._lfsr_table) - 1
            lfsr_indices = (self._lfsr_pos + (np.arange(num_samples, dtype=np.float64) * step_inc).astype(np.int32)) & lfsr_mask
            self._lfsr_pos = int((self._lfsr_pos + int(num_samples * step_inc) + 1) & lfsr_mask)
            noise_wave = self._lfsr_table[lfsr_indices]
        else:
            noise_wave = np.ones(num_samples, dtype=np.int32)

        # 4. Mezclador del AY-3-8912 (puerta lógica AND entre tono y ruido) y conversión DAC
        mixed_wave = tone_wave & noise_wave
        final_wave = (mixed_wave * amplitudes) - (amplitudes // 2)
        audio_data = final_wave.astype(np.int16)

        if pygame.mixer.get_init():
            if pygame.mixer.get_init()[2] == 2:
                audio_data = np.column_stack((audio_data, audio_data))
            audio_data = np.ascontiguousarray(audio_data)
            return pygame.sndarray.make_sound(audio_data)
        return None

    def play_sound(self, channel_status, period, duration, volume, env=0, ent=0, noise=0, blocking=True):
        """Encola un sonido según la especificación exacta de SOUND QUEUE (&BCAA) en sound.asm."""
        if not pygame.mixer.get_init():
            return True

        # SOUND QUEUE llama primero a SOUND CONTINUE (sound.asm línea 332)
        if self.global_held:
            self.continue_all()

        target_mask = int(channel_status) & 7
        if target_mask == 0:
            # sound.asm líneas 334-335: and $07 : scf : ret z
            return True

        flush = bool(channel_status & 128)
        hold_flag = bool(channel_status & 64)
        # sound.asm líneas 363-369: combina bits de rendezvous explícitos (bits 3..5)
        # con los canales destino (bits 0..2) para sincronizar sonidos multicanal
        combined_rv = ((int(channel_status) >> 3) | target_mask) & 7

        target_channels = [c_id for c_id in range(3) if (target_mask & (1 << c_id))]

        if pygame.mixer.get_num_channels() < 3:
            pygame.mixer.set_num_channels(3)

        # Si hay flush (bit 7), limpiar los canales indicados antes de comprobar espacio
        if flush:
            for c_id in target_channels:
                self._flush_channel(c_id)

        # Desarmar eventos ON SQ en los canales destino (sound.asm línea 352)
        for c_id in target_channels:
            self.sq_events_armed[c_id] = False

        # Actualizar estado de las colas antes de comprobar huecos libres
        self.update_queues()

        # En BASIC, si alguna de las colas de destino (de 4 slots en espera) está llena,
        # el comando SOUND espera hasta que haya al menos 1 hueco libre en todos los canales destino
        if not flush:
            if not blocking:
                for c_id in target_channels:
                    if len(self.channel_queues[c_id]) >= 4:
                        return False
            else:
                while any(len(self.channel_queues[c_id]) >= 4 for c_id in target_channels):
                    try:
                        pygame.event.pump()
                    except Exception:
                        pass
                    pygame.time.wait(5)
                    self.update_queues()

        # Sintetizar sonido y encolar en cada canal destino (manteniendo fase continua por canal)
        for c_id in target_channels:
            sound_obj = self._synthesize_sound(c_id, period, duration, volume, env, ent, noise)
            if sound_obj is None:
                continue
            self_bit = 1 << c_id
            rv_mask = combined_rv & (~self_bit & 7)
            item = {
                'sound': sound_obj,
                'hold': hold_flag,
                'rendezvous': rv_mask,
                'prequeued': False
            }
            self.channel_queues[c_id].append(item)

        self.update_queues()
        return True

    def _flush_channel(self, c_id):
        """Limpia la cola y detiene el canal c_id (_sound_reset_27 en sound.asm)."""
        try:
            pygame.mixer.Channel(c_id).stop()
        except Exception:
            pass
        self.channel_queues[c_id].clear()
        self.channel_status_byte[c_id] = 0
        self.channel_held[c_id] = False
        self.sq_events_armed[c_id] = False
        self.sq_events_pending[c_id] = False

    def _start_head_item(self, c_id):
        """Extrae el elemento en la cabeza de la cola de c_id y comienza su reproducción (_process_queue_item_15)."""
        if not self.channel_queues[c_id]:
            self.channel_status_byte[c_id] = 0
            self.channel_held[c_id] = False
            return

        item = self.channel_queues[c_id].pop(0)
        self.channel_status_byte[c_id] = 16  # Bit 4 ($10) -> bit 7 ($80 = 128) en SOUND_CHECK
        self.channel_held[c_id] = False
        pg_chan = pygame.mixer.Channel(c_id)
        if not item.get('prequeued', False):
            pg_chan.play(item['sound'])

        # Si el siguiente elemento en la cola no tiene hold ni rendezvous, pre-encolarlo en Pygame
        # para transición sin huecos (gapless), manteniéndolo en channel_queues hasta que empiece
        if self.channel_queues[c_id]:
            nxt = self.channel_queues[c_id][0]
            if not nxt['hold'] and nxt['rendezvous'] == 0 and not nxt['prequeued']:
                if pg_chan.get_busy() and pg_chan.get_queue() is None:
                    pg_chan.queue(nxt['sound'])
                    nxt['prequeued'] = True

    def update_queues(self):
        """Actualiza el estado de reproducción, colas, Hold y Rendezvous de los 3 canales."""
        if not pygame.mixer.get_init() or not hasattr(self, 'channel_queues'):
            return
        if getattr(self, 'global_held', False):
            return

        # Paso 1: Comprobar si sonidos activos o pre-encolados han terminado / transicionado
        for c_id in range(3):
            pg_chan = pygame.mixer.Channel(c_id)
            busy = pg_chan.get_busy()

            # Si el primer elemento de channel_queues estaba pre-encolado en Pygame:
            if self.channel_queues[c_id] and self.channel_queues[c_id][0].get('prequeued', False):
                if not busy:
                    # Tanto el sonido anterior como el pre-encolado terminaron
                    self.channel_queues[c_id].pop(0)
                    self.channel_status_byte[c_id] = 0
                elif pg_chan.get_queue() is None:
                    # El sonido anterior terminó y el pre-encolado ya está sonando activamente
                    self.channel_queues[c_id].pop(0)
                    self.channel_status_byte[c_id] = 16

            # Si el canal estaba en estado reproduciendo (16) y ya no está ocupado en Pygame:
            if self.channel_status_byte[c_id] == 16 and not pg_chan.get_busy():
                self.channel_status_byte[c_id] = 0

        # Paso 2: Procesar cabeza de cola para canales que están libres (status == 0)
        for c_id in range(3):
            if self.channel_status_byte[c_id] == 0 and self.channel_queues[c_id]:
                head = self.channel_queues[c_id][0]
                if head['hold']:
                    # sound.asm líneas 690-691: res 3,(hl) ; ld (ix+$03),$08
                    head['hold'] = False
                    self.channel_status_byte[c_id] = 8  # Held ($08 << 3 = 64)
                    self.channel_held[c_id] = True
                elif head['rendezvous'] != 0:
                    # Poner canal en espera de rendezvous (1..7)
                    self.channel_status_byte[c_id] = head['rendezvous'] & 7
                else:
                    self._start_head_item(c_id)

        # Paso 3: Resolver grupos de Rendezvous cuando todos los canales implicados están listos
        for c_id in range(3):
            rv = self.channel_status_byte[c_id]
            if 1 <= rv <= 7:
                self_bit = 1 << c_id
                group_mask = rv | self_bit
                ready = True
                for other_id in range(3):
                    other_bit = 1 << other_id
                    if (group_mask & other_bit) and other_id != c_id:
                        other_rv = self.channel_status_byte[other_id]
                        if not (1 <= other_rv <= 7) or not (other_rv & self_bit):
                            ready = False
                            break
                if ready:
                    for member_id in range(3):
                        if group_mask & (1 << member_id):
                            if self.channel_queues[member_id]:
                                self.channel_queues[member_id][0]['rendezvous'] = 0
                            self._start_head_item(member_id)

        # Paso 4: Si algún canal tenía evento ON SQ armado y ahora tiene hueco libre (< 4 en cola),
        # disparar evento síncrono (_process_queue_item_53 en sound.asm líneas 676-684)
        for c_id in range(3):
            if self.sq_events_armed.get(c_id, False) and len(self.channel_queues[c_id]) < 4:
                self.sq_events_armed[c_id] = False
                self.sq_events_pending[c_id] = True

        # Paso 5: Asegurar que si un canal está reproduciendo y el siguiente item en cola
        # es normal (sin hold ni rendezvous), esté pre-encolado en Pygame para transición gapless
        for c_id in range(3):
            if self.channel_status_byte[c_id] == 16 and self.channel_queues[c_id]:
                nxt = self.channel_queues[c_id][0]
                if not nxt['hold'] and nxt['rendezvous'] == 0 and not nxt['prequeued']:
                    pg_chan = pygame.mixer.Channel(c_id)
                    if pg_chan.get_busy() and pg_chan.get_queue() is None:
                        pg_chan.queue(nxt['sound'])
                        nxt['prequeued'] = True

    def release_channels(self, channels):
        """SOUND RELEASE (&BCB3): Libera canales actualmente en estado Hold (cabeza de cola) y reanuda sonido."""
        if self.global_held:
            self.continue_all()
        mask = int(channels) & 7
        for c_id in range(3):
            if mask & (1 << c_id):
                if self.channel_status_byte[c_id] == 8 or self.channel_held.get(c_id, False):
                    self.channel_status_byte[c_id] = 0
                    self.channel_held[c_id] = False
        self.update_queues()

    def hold_all(self):
        """SOUND HOLD (&BCB6): Pausa inmediatamente todos los canales activos."""
        self.update_queues()
        any_active = any(self.channel_status_byte[c] == 16 for c in range(3))
        if any_active and pygame.mixer.get_init():
            self.global_held = True
            pygame.mixer.pause()
            return True
        return False

    def continue_all(self):
        """SOUND CONTINUE (&BCB9): Reanuda todos los canales tras SOUND HOLD."""
        if self.global_held and pygame.mixer.get_init():
            self.global_held = False
            pygame.mixer.unpause()
        self.update_queues()

    def write_psg_register(self, reg, val):
        """MC SOUND REGISTER (&BD34): Escribe un valor en un registro del AY-3-8912."""
        reg = int(reg) & 0x0F
        val = int(val) & 0xFF
        self.psg_registers[reg] = val

    def arm_sq_event(self, channel):
        """SOUND ARM EVENT (&BCB0, sound.asm líneas 544-576):
        Si la cola del canal tiene al menos 1 hueco libre, dispara el evento inmediatamente
        (sq_events_pending = True) y deja sq_events_armed = False.
        Si la cola está llena (0 huecos libres), arma sq_events_armed = True para cuando quede un hueco.
        """
        self.update_queues()
        c_id = 0
        if channel & 1:
            c_id = 0
        elif channel & 2:
            c_id = 1
        elif channel & 4:
            c_id = 2
        else:
            return

        self.sq_events_armed[c_id] = False
        free = max(0, 4 - len(self.channel_queues[c_id]))
        if free > 0:
            self.sq_events_pending[c_id] = True
        else:
            self.sq_events_armed[c_id] = True

    def get_sq_status(self, channel, disarm=True):
        """SOUND CHECK (&BCAD) / Función BASIC SQ(channel):
        channel: 1 (A), 2 (B), 4 (C).
        Bits 0..2: Huecos libres en la cola de espera (0..4)
        Bits 3..5: Estado de Rendezvous (8=A, 16=B, 32=C)
        Bit 6 (64): Canal en Hold
        Bit 7 (128): Canal reproduciendo un sonido activamente
        """
        self.update_queues()

        c_id = 0
        if channel & 1:
            c_id = 0
        elif channel & 2:
            c_id = 1
        elif channel & 4:
            c_id = 2

        if disarm:
            # sound.asm línea 517: SOUND CHECK desarma el evento ON SQ del canal consultado
            self.sq_events_armed[c_id] = False

        free = max(0, 4 - len(self.channel_queues[c_id]))
        status = (free & 7) | ((self.channel_status_byte[c_id] & 0x1F) << 3)
        return status
