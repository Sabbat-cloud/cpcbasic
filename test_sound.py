import pygame
import numpy as np

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
t = np.linspace(0, 1, 44100)
wave = (32767 * np.sin(2 * np.pi * 440 * t)).astype(np.int16)
wave = np.column_stack((wave, wave))
wave = np.ascontiguousarray(wave)
sound = pygame.sndarray.make_sound(wave)
sound.play()
pygame.time.wait(1000)
print("Done playing!")
