import numpy as np
import wave
from audio.sound import SoundEngine
import pygame

pygame.init()
engine = SoundEngine()
engine.set_env(1, [5, 2, 2, 10, -1, 5])
engine.set_ent(1, [5, 1, 3, 5, -1, 3])

all_audio = []
old_make_sound = pygame.sndarray.make_sound

def capture_sound(audio_data):
    all_audio.append(audio_data.copy())
    return old_make_sound(audio_data)

pygame.sndarray.make_sound = capture_sound

engine.play_sound(65, 190, 20, 14, 1, 1, 0)
engine.release_channels(7)

if all_audio:
    concatenated = np.concatenate(all_audio, axis=0)
    print("Max amplitude:", np.max(concatenated))
    
    with wave.open("d:\\cpcbasic\\test_output.wav", "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(44100)
        w.writeframes(concatenated.tobytes())
    print("Wrote test_output.wav!")
else:
    print("No audio captured!")
