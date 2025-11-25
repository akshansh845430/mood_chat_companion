import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint
from build_model import build_emotion_model

# Emotion mapping for your dataset's folder order
EMOTION_MAP = {
    "angry": 0,
    "happy": 1,
    "neutral": 2,
    "sad": 3
}

def extract_mfcc(file_path, max_pad_len=200):
    """Extract MFCC from an audio file and pad/truncate to 40x200."""
    audio, sr = librosa.load(file_path, sr=22050)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)

    # Pad or truncate
    if mfcc.shape[1] < max_pad_len:
        pad_width = max_pad_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :max_pad_len]

    return mfcc

def load_dataset(folder="../../data/processed"):

    X, y = [], []

    for emotion in os.listdir(folder):
        emotion_folder = os.path.join(folder, emotion)

        if not os.path.isdir(emotion_folder):
            continue

        if emotion not in EMOTION_MAP:
            print("Skipping unknown folder:", emotion)
            continue

        label = EMOTION_MAP[emotion]

        for file in os.listdir(emotion_folder):
            if file.endswith(".wav"):
                file_path = os.path.join(emotion_folder, file)
                mfcc = extract_mfcc(file_path)
                X.append(mfcc)
                y.append(label)

    X = np.array(X)               # shape (samples, 40, 200)
    X = np.transpose(X, (0, 2, 1))  # shape (samples, 200, 40)
    y = np.array(y)

    return X, y


def train():
    print("📥 Loading dataset...")
    X, y = load_dataset()

    print("Dataset loaded:", X.shape, y.shape)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = build_emotion_model(input_shape=(200, 40), num_classes=4)

    checkpoint = ModelCheckpoint(
        "emotion_model.h5",
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )

    print("🚀 Starting training...")
    model.fit(
        X_train,
        y_train,
        epochs=40,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=[checkpoint]
    )

    print("🎉 Training complete. Best model saved as emotion_model.h5")


if __name__ == "__main__":
    train()
