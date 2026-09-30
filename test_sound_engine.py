import pygame
from audio.sound import SoundEngine

pygame.init()
engine = SoundEngine()

engine.set_env(1, [5, 2, 2, 10, -1, 5])
engine.set_ent(1, [5, 1, 3, 5, -1, 3])

for i in range(15):
    print(f"Loop {i+1}")
    dur = 20
    if i == 14: dur = 40
    
    # Trace inside play_sound loop
    print(f"A -> Playing {190}...")
    engine.play_sound(65, 190, dur, 14, 1, 1, 0)
    print(f"B -> Playing {480}...")
    engine.play_sound(66, 480, dur, 10, 1, 0, 0)
    print(f"C -> Playing {0}...")
    engine.play_sound(68, 0, dur, 12, 2, 2, 10)
    
    print(f"Releasing...")
    engine.release_channels(7)
    
print("Done!")
