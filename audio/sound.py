import pygame
import numpy as np

class SoundEngine:
    def __init__(self, sample_rate=44100):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=sample_rate, size=-16, channels=2, buffer=1024)
        
        self.sample_rate = sample_rate
        # Interrupción del firmware del CPC (aprox 300Hz)
        self.cpc_int_freq = 300.0
        self.samples_per_tick = int(self.sample_rate / self.cpc_int_freq)
        
        self.envelopes_vol = {}
        self.envelopes_tone = {}
        
        # LUT (Look-Up Table) logarítmica exacta del DAC del AY-3-8912 (16-bit)
        self.AY_VOL_LUT = np.array([
            0, 235, 335, 474, 679, 959, 1373, 1944, 
            2783, 3965, 5606, 7949, 11283, 15998, 22699, 32767
        ], dtype=np.int16)

    def set_env(self, env_no, sections):
        # sections es una lista plana desde el parser
        grouped = []
        for i in range(0, len(sections), 3):
            chunk = sections[i:i+3]
            while len(chunk) < 3: chunk.append(0)
            grouped.append(chunk)
        self.envelopes_vol[env_no] = grouped

    def set_ent(self, ent_no, sections):
        grouped = []
        for i in range(0, len(sections), 3):
            chunk = sections[i:i+3]
            while len(chunk) < 3: chunk.append(0)
            grouped.append(chunk)
        self.envelopes_tone[ent_no] = grouped

    def _calc_env_ticks(self, env_no, is_tone=False):
        """Calcula cuántos ticks de 300Hz dura una envolvente completa."""
        envs = self.envelopes_tone if is_tone else self.envelopes_vol
        if env_no not in envs:
            return 0
            
        total_ticks = 0
        for section in envs[env_no]:
            steps, _, pause_time = section
            # pause_time está en 1/100s. 0 significa 256. (1/100s = 3 ticks a 300Hz)
            if pause_time == 0: pause_time = 256
            ticks_per_step = pause_time * 3 
            
            # Si steps == 0 es una asignación absoluta, toma 1 'step' de tiempo
            actual_steps = max(1, steps)
            total_ticks += actual_steps * ticks_per_step
            
        return total_ticks

    def play_sound(self, channel_status, period, duration, volume, env=0, ent=0, noise=0):
        # 1. Resolver duración en Ticks (300Hz)
        if duration > 0:
            # Duración en 1/100s -> convertir a ticks de 300Hz (* 3)
            total_ticks = duration * 3
        else:
            # duration <= 0 depende de la longitud de la envolvente de volumen
            env_ticks = self._calc_env_ticks(env, is_tone=False)
            if env_ticks == 0:
                env_ticks = 60 # Fallback si no hay envolvente (20 * 3 = 1/5 seg)
                
            if duration == 0:
                total_ticks = env_ticks
            else: # duration < 0 repite la envolvente abs(duration) veces
                total_ticks = env_ticks * abs(duration)
                
        if total_ticks <= 0:
            return

        # 2. Generar Arrays de Periodo y Volumen a 300Hz (Staircasing)
        tick_vols = np.full(total_ticks, volume, dtype=float)
        tick_periods = np.full(total_ticks, period, dtype=float)

        # Aplicar ENV (Volumen)
        if env > 0 and env in self.envelopes_vol:
            current_vol = volume
            t_idx = 0
            
            # Si duration < 0, repetimos la envolvente
            repeats = abs(duration) if duration < 0 else 1
            
            for _ in range(repeats):
                for section in self.envelopes_vol[env]:
                    steps, step_size, pause_time = section
                    if pause_time == 0: pause_time = 256
                    ticks_per_step = pause_time * 3
                    
                    is_absolute = (steps == 0)
                    actual_steps = max(1, steps)
                    
                    for step in range(actual_steps):
                        if t_idx >= total_ticks: break
                        
                        if is_absolute:
                            current_vol = step_size
                        else:
                            current_vol += step_size
                            
                        # El hardware del CPC hace loop en volumen 0-15
                        current_vol = current_vol % 16
                        
                        end_t = min(t_idx + ticks_per_step, total_ticks)
                        tick_vols[t_idx:end_t] = current_vol
                        t_idx = end_t

        # Aplicar ENT (Tono)
        if ent > 0 and ent in self.envelopes_tone:
            current_period = period
            t_idx = 0
            
            for section in self.envelopes_tone[ent]:
                steps, step_size, pause_time = section
                if pause_time == 0: pause_time = 256
                ticks_per_step = pause_time * 3
                
                is_absolute = (steps == 0)
                actual_steps = max(1, steps)
                
                for step in range(actual_steps):
                    if t_idx >= total_ticks: break
                    
                    if is_absolute:
                        current_period = step_size
                    else:
                        current_period += step_size
                        
                    if current_period < 0: current_period = 0
                    if current_period > 4095: current_period = 4095 # Límite hardware AY
                    
                    end_t = min(t_idx + ticks_per_step, total_ticks)
                    tick_periods[t_idx:end_t] = current_period
                    t_idx = end_t

        # 3. Expandir Ticks a Samples de Audio
        num_samples = total_ticks * self.samples_per_tick
        
        # Expandir volúmenes y convertirlos mediante la LUT logarítmica
        expanded_vols = np.repeat(tick_vols, self.samples_per_tick)
        expanded_vols = np.clip(expanded_vols, 0, 15).astype(int)
        amplitudes = self.AY_VOL_LUT[expanded_vols]

        # Expandir periodos y convertirlos a frecuencia (F = 62500 / P)
        expanded_periods = np.repeat(tick_periods, self.samples_per_tick)
        # Evitar división por cero; si P=0 la frecuencia es 0
        freqs = np.divide(62500.0, expanded_periods, out=np.zeros_like(expanded_periods), where=expanded_periods!=0)

        # 4. Generación de Ondas (Digital Logic 0 o 1)
        # Onda de Tono
        phase = np.cumsum(freqs) * (2 * np.pi / self.sample_rate)
        # El AY genera una onda cuadrada, la representamos como 0 y 1 para el mezclador
        tone_wave = (np.sin(phase) >= 0).astype(int)
        if period == 0 and ent == 0:
            tone_wave = np.ones(num_samples, dtype=int) # Si no hay tono, canal abierto (1)

        # Onda de Ruido (Pseudo-LFSR)
        if noise > 0:
            noise_freq = 62500.0 / noise
            chunk_size = max(1, int(self.sample_rate / noise_freq))
            num_chunks = (num_samples // chunk_size) + 1
            # Random 0 o 1 simula muy fielmente el LFSR a esta resolución
            rand_vals = np.random.randint(0, 2, num_chunks)
            noise_wave = np.repeat(rand_vals, chunk_size)[:num_samples]
        else:
            noise_wave = np.ones(num_samples, dtype=int) # Si no hay ruido, canal abierto (1)

        # 5. Mezclador (AND lógico) y DAC
        # El AY-3-8912 mezcla Tono y Ruido usando compuertas AND antes del volumen
        mixed_wave = tone_wave & noise_wave
        
        # Aplicar el volumen al mezclador
        final_wave = mixed_wave * amplitudes
        
        # Eliminar el offset DC (AC coupling) para evitar chasquidos en altavoces modernos
        final_wave = final_wave - (amplitudes // 2)

        # 6. Preparar y Reproducir
        audio_data = final_wave.astype(np.int16)
        
        # Duplicar a estéreo para Pygame
        if pygame.mixer.get_init()[2] == 2:
            audio_data = np.column_stack((audio_data, audio_data))
            
        audio_data = np.ascontiguousarray(audio_data)
        sound = pygame.sndarray.make_sound(audio_data)
        
        # Lógica de channel_status (Bits 0-7)
        chan_a = channel_status & 1
        chan_b = (channel_status & 2) >> 1
        chan_c = (channel_status & 4) >> 2
        flush = (channel_status & 128) >> 7
        
        # Determinar canales de destino
        target_channels = []
        if chan_a: target_channels.append(0)
        if chan_b: target_channels.append(1)
        if chan_c: target_channels.append(2)
        if not target_channels:
            target_channels.append(0) # Default A

        # Pygame necesita tener al menos 3 canales configurados
        if pygame.mixer.get_num_channels() < 3:
            pygame.mixer.set_num_channels(3)

        if not hasattr(self, 'channel_held'):
            self.channel_held = {0: False, 1: False, 2: False}
        if not hasattr(self, 'channel_queues'):
            self.channel_queues = {0: [], 1: [], 2: []}

        for c_id in target_channels:
            pg_chan = pygame.mixer.Channel(c_id)
            if flush:
                pg_chan.stop()
                self.channel_held[c_id] = False
                self.channel_queues[c_id].clear()
                
            hold_flag = (channel_status & 64) > 0
            if hold_flag:
                self.channel_held[c_id] = True

            # El CPC real bloquea la ejecución si la cola (de hasta 4 sonidos) está llena.
            while len(self.channel_queues[c_id]) + (1 if pg_chan.get_busy() else 0) + (1 if pg_chan.get_queue() else 0) >= 4:
                pygame.time.wait(10)
                self.update_queues()
                
            self.channel_queues[c_id].append(sound)
            self.update_queues()

    def update_queues(self):
        if not hasattr(self, 'channel_queues'): return
        for c in range(3):
            if self.channel_held[c]:
                continue
            pg_chan = pygame.mixer.Channel(c)
            # Si el canal está libre y tenemos en la cola virtual
            if not pg_chan.get_busy() and len(self.channel_queues[c]) > 0:
                nxt_sound = self.channel_queues[c].pop(0)
                pg_chan.play(nxt_sound)
            # Si el canal está ocupado pero la cola interna de pygame está libre
            elif pg_chan.get_busy() and pg_chan.get_queue() is None and len(self.channel_queues[c]) > 0:
                nxt_sound = self.channel_queues[c].pop(0)
                pg_chan.queue(nxt_sound)

    def release_channels(self, channels):
        if not hasattr(self, 'channel_held'):
            self.channel_held = {0: False, 1: False, 2: False}
        if channels & 1: self.channel_held[0] = False
        if channels & 2: self.channel_held[1] = False
        if channels & 4: self.channel_held[2] = False
        self.update_queues()

    def get_sq_status(self, channel):
        if not hasattr(self, 'channel_held'):
            self.channel_held = {0: False, 1: False, 2: False}
        if not hasattr(self, 'channel_queues'):
            self.channel_queues = {0: [], 1: [], 2: []}
            
        c_id = 0
        if channel == 2: c_id = 1
        elif channel == 4: c_id = 2
        
        pg_chan = pygame.mixer.Channel(c_id)
        
        status = 0
        # Bits 0-2: Entradas libres en la cola (máx 4)
        used = len(self.channel_queues[c_id])
        if pg_chan.get_busy(): used += 1
        if pg_chan.get_queue() is not None: used += 1
        free = max(0, 4 - used)
        status |= (free & 7)
        
        # Bit 6: Hold state
        if self.channel_held[c_id]:
            status |= 64
            
        # Bit 7: Active
        if pg_chan.get_busy() or len(self.channel_queues[c_id]) > 0:
            status |= 128
            
        return status
