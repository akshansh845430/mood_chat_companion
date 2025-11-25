import sounddevice as sd
from scipy.io.wavfile import read

def play_audio(file_path):
    try:
        rate, data = read(file_path)
        sd.play(data, rate)
        sd.wait()
        print("\n🎧 Playback finished.\n")
    except Exception as e:
        print("Error playing audio:", e)
