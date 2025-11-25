from features.mfcc_extractor import extract_mfcc
from models.predict import predict_emotion
import numpy as np
import os

def run_full_pipeline_test():
    print("\n🔍 Running FULL PIPELINE TEST...\n")

    test_audio = "../data/audio_samples/sample_20251124_224355.wav"

    if not os.path.exists(test_audio):
        print(f"❌ Test audio not found at {test_audio}")
        return

    # Step 1: MFCC extraction
    mfcc = extract_mfcc(test_audio)
    if mfcc is None:
        print("❌ MFCC extraction failed.")
        return

    print("✅ MFCC extracted. Shape =", mfcc.shape)

    # Step 2: Prediction → using our actual tuple return
    emotion, probabilities = predict_emotion(test_audio)

    print("\n-----------------------------")
    print(f"Predicted Emotion: {emotion}")
    print(f"Probabilities: {probabilities}")
    print("-----------------------------\n")


if __name__ == "__main__":
    run_full_pipeline_test()
