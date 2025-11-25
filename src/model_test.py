from models.build_model import build_emotion_model

def test_model():
    # No arguments – uses default (40,200)
    model = build_emotion_model()
    model.summary()

if __name__ == "__main__":
    test_model()

