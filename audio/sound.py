import pygame
import numpy as np

class SoundEngine:
    def __init__(self):
        # Only initialize if pygame isn't already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
        self.sample_rate = 44100
        
    def play_sound(self, channel, period, duration, volume, env=0, ent=0, noise=0):
        if period == 0 or duration == 0:
            return
            
        # Frequency calculation based on CPC manual: period = 62500 / freq
        freq = 62500.0 / period
        duration_sec = duration / 100.0
        
        num_samples = int(self.sample_rate * duration_sec)
        t = np.linspace(0, duration_sec, num_samples, endpoint=False)
        
        # Square wave synthesis
        wave = np.sign(np.sin(2 * np.pi * freq * t))
        
        # Inject white noise
        if noise > 0:
            noise_amp = noise / 30.0  # noise param 0-30 in BASIC 1.1
            noise_wave = np.random.uniform(-1, 1, num_samples) * noise_amp
            wave = wave + noise_wave
            
        # Scale to 16-bit audio
        amp = (volume / 15.0) * 32000
        wave = np.clip(wave * amp, -32768, 32767).astype(np.int16)
        
        # Ensure correct shape for the mixer
        mixer_init = pygame.mixer.get_init()
        if mixer_init:
            _, _, channels = mixer_init
            if channels == 2:
                wave = np.column_stack((wave, wave))
        
        sound = pygame.sndarray.make_sound(wave)
        sound.play()
