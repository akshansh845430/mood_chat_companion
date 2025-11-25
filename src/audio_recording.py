from utils.playback import play_audio
import sounddevice as sd
import soundfile as sf
import numpy as np
import os
from datetime import datetime

def record_audio(folder=None):
    """Record audio until ENTER is pressed and save it as a WAV file."""
    
    if folder is None:
        folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "audio_samples"))
    os.makedirs(folder, exist_ok=True)

    filename = datetime.now().strftime("sample_%Y%m%d_%H%M%S.wav")
    filepath = os.path.join(folder, filename)

    sample_rate = 16000
    print("\n🎙 Recording... Press ENTER to stop.\n")

    recorded_chunks = []

    def callback(indata, frames, time, status):
        recorded_chunks.append(indata.copy())

    # Start stream
    stream = sd.InputStream(samplerate=sample_rate, channels=1, callback=callback)
    with stream:
        input()  # wait for ENTER press

    # Save audio
    audio = np.concatenate(recorded_chunks, axis=0)
    sf.write(filepath, audio, sample_rate)
    
    print(f"✔ Saved audio at: {filepath}\n")
    return filepath


if __name__ == "__main__":
    audio_file = record_audio()
    play_audio(audio_file)
