from models.predict import predict_emotion
import numpy as np

def run_test():
    test_audio = "../data/audio_samples/sample_20251124_225334.wav"  # change path if needed
    # D:\mood_chat_companion\data\audio_samples\sample_20251124_225334.wav

    print("\n🎧 Running Prediction Test...")
    emotion, probs = predict_emotion(test_audio)

    print("\n-----------------------------")
    print("Predicted Emotion:", emotion)
    print("Probabilities:", probs)
    print("-----------------------------")

if __name__ == "__main__":
    run_test()
