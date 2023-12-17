import numpy as np
import sounddevice as sd



def voice():
    duration = 10 #in seconds

    def audio_callback(indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        print( int(volume_norm))

    stream = sd.InputStream(callback=audio_callback)
    with stream:
        sd.sleep(duration * 100000)

voice()

