import pygame
import numpy as np

class SoundEngine:
    def __init__(self):
        # Only initialize if pygame isn't already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        self.sample_rate = 44100
        self.envelopes_vol = {}
        self.envelopes_tone = {}
        
    def set_env(self, env_no, sections):
        # sections format: [step_count, step_height, step_duration, ...]
        self.envelopes_vol[env_no] = sections
        
    def set_ent(self, ent_no, sections):
        # sections format: [step_count, step_height, step_duration, ...]
        self.envelopes_tone[ent_no] = sections

    def play_sound(self, channel, period, duration, volume, env=0, ent=0, noise=0):
        if period == 0 or duration == 0:
            return
            
        duration_sec = duration / 100.0
        num_samples = int(self.sample_rate * duration_sec)
        t = np.linspace(0, duration_sec, num_samples, endpoint=False)
        
        # Base frequency array
        freq_base = 62500.0 / period if period > 0 else 0
        freqs = np.full(num_samples, freq_base)
        
        # Apply tone envelope
        if ent > 0 and ent in self.envelopes_tone:
            sections = self.envelopes_tone[ent]
            current_sample = 0
            current_period = period
            for i in range(0, len(sections), 3):
                if i + 2 >= len(sections): break
                steps = sections[i]
                height = sections[i+1] # period change per step
                step_dur = sections[i+2]
                if step_dur == 0: step_dur = 256
                step_samples = int(self.sample_rate * (step_dur / 100.0))
                
                for step in range(steps):
                    end_sample = current_sample + step_samples
                    if end_sample > num_samples:
                        end_sample = num_samples
                    if end_sample > current_sample:
                        current_period += height
                        if current_period < 0: current_period = 0
                        f = 62500.0 / current_period if current_period > 0 else 0
                        freqs[current_sample:end_sample] = f
                    current_sample = end_sample
                    if current_sample >= num_samples:
                        break
                if current_sample >= num_samples:
                    break
        
        # Base volume array
        vols = np.full(num_samples, float(volume))
        
        # Apply volume envelope
        if env > 0 and env in self.envelopes_vol:
            sections = self.envelopes_vol[env]
            current_sample = 0
            current_vol = volume
            for i in range(0, len(sections), 3):
                if i + 2 >= len(sections): break
                steps = sections[i]
                height = sections[i+1]
                step_dur = sections[i+2]
                if step_dur == 0: step_dur = 256
                step_samples = int(self.sample_rate * (step_dur / 100.0))
                
                for step in range(steps):
                    end_sample = current_sample + step_samples
                    if end_sample > num_samples:
                        end_sample = num_samples
                    if end_sample > current_sample:
                        current_vol += height
                        if current_vol > 15: current_vol = 0 # Hardware loops around
                        if current_vol < 0: current_vol = 15
                        vols[current_sample:end_sample] = current_vol
                    current_sample = end_sample
                    if current_sample >= num_samples:
                        break
                if current_sample >= num_samples:
                    break
                    
            # Si la nota sigue sonando pero el envolvente terminó, se mantiene el último volumen
            if current_sample < num_samples:
                vols[current_sample:] = current_vol

        # Integration of frequencies to get phase
        phase = np.cumsum(freqs) * (2 * np.pi / self.sample_rate)
        wave = np.sign(np.sin(phase))
        
        # Inject white noise
        if noise > 0:
            noise_amp = noise / 31.0
            noise_wave = np.random.uniform(-1, 1, num_samples) * noise_amp
            wave = wave + noise_wave
            
        # Scale to 16-bit audio
        amp = (vols / 15.0) * 32000
        wave = np.clip(wave * amp, -32768, 32767).astype(np.int16)
        
        # Ensure correct shape for the mixer
        mixer_init = pygame.mixer.get_init()
        if mixer_init:
            _, _, channels = mixer_init
            if channels == 2:
                wave = np.column_stack((wave, wave))
                
        wave = np.ascontiguousarray(wave)
        sound = pygame.sndarray.make_sound(wave)
        sound.play()
