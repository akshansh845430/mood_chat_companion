import numpy as np
from tensorflow.keras.models import load_model
from features.mfcc_extractor import extract_mfcc

EMOTIONS = ["angry", "happy", "neutral", "sad"]

def predict_emotion(file_path, model_path="emotion_model.h5"):
    # 1. Extract MFCC
    mfcc = extract_mfcc(file_path)

    if mfcc is None:
        return None, None

    # Convert MFCC (40,200) -> (200,40)
    mfcc = np.transpose(mfcc, (1, 0))

    # Add batch dimension -> (1, 200, 40)
    mfcc = np.expand_dims(mfcc, axis=0)

    # 2. Load model
    try:
        model = load_model(model_path)
    except Exception as e:
        print("⚠️ Could not load model, using random output:", e)
        probs = np.random.rand(4)
        probs = probs / np.sum(probs)
        return EMOTIONS[np.argmax(probs)], probs

    # 3. Predict
    probs = model.predict(mfcc)[0]
    predicted_index = np.argmax(probs)
    emotion = EMOTIONS[predicted_index]

    return emotion, probs
