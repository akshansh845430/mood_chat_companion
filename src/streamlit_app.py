# src/streamlit_app.py
import streamlit as st
import sounddevice as sd
import soundfile as sf
import os
from models.predict import predict_emotion
from utils.emotion_responder import get_response
from utils.tts_engine import speak   # neural TTS
from utils.user_name_memory import get_name, set_name, FILE as NAME_FILE

# ---------------------------------------------
# Config & paths
# ---------------------------------------------
st.set_page_config(page_title="Mood Companion", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "..", "data", "audio_samples")
MODEL_PATH = os.path.join(BASE_DIR, "models", "emotion_model.h5")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)  # safe-guard if user hasn't created it

# Use your uploaded screenshot as a safe fallback avatar (local path available in session)
FALLBACK_AVATAR = "/mnt/data/Screenshot 2025-11-25 091414.png"

AVATAR_MAP = {
    "neutral": os.path.join(ASSETS_DIR, "avatar_neutral.gif") if os.path.exists(os.path.join(ASSETS_DIR, "avatar_neutral.gif")) else FALLBACK_AVATAR,
    "happy":   os.path.join(ASSETS_DIR, "avatar_happy.gif")   if os.path.exists(os.path.join(ASSETS_DIR, "avatar_happy.gif"))   else FALLBACK_AVATAR,
    "sad":     os.path.join(ASSETS_DIR, "avatar_sad.gif")     if os.path.exists(os.path.join(ASSETS_DIR, "avatar_sad.gif"))     else FALLBACK_AVATAR,
    "angry":   os.path.join(ASSETS_DIR, "avatar_angry.gif")   if os.path.exists(os.path.join(ASSETS_DIR, "avatar_angry.gif"))   else FALLBACK_AVATAR,
}

# ---------------------------------------------
# UI: header, avatar, controls
# ---------------------------------------------
st.markdown("<h1 style='text-align:center; color:#f3a742;'>Your Mood Companion</h1>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1])

with col_left:
    avatar_placeholder = st.empty()
    # show neutral avatar (or fallback)
    avatar_placeholder.image(AVATAR_MAP["neutral"], width=320)

    status_box = st.empty()
    probs_box = st.empty()
    st.markdown("---")
    st.write("Stored name (if any):")

    # Display / change stored name
    stored = get_name()
    name_input = st.text_input("Your name (optional)", value=stored or "")
    save_col, forget_col = st.columns([1, 1])
    with save_col:
        if st.button("Save name"):
            if name_input and name_input.strip():
                set_name(name_input.strip())
                st.success(f"Saved name: {name_input.strip()}")
                stored = name_input.strip()
            else:
                st.warning("Please enter a non-empty name to save.")
    with forget_col:
        if st.button("Forget name"):
            # delete memory file if present
            try:
                if os.path.exists(NAME_FILE):
                    os.remove(NAME_FILE)
                stored = None
                st.success("Name forgotten.")
            except Exception as e:
                st.error(f"Could not forget name: {e}")

with col_right:
    st.write("Quick controls")
    st.markdown("**Record (4 seconds)** — click to record, then model will run and assistant will reply.")
    record_btn = st.button("🎙 Record (4s)", use_container_width=True)
    st.markdown("---")
    st.write("Notes:")
    st.write("- Allow microphone access when prompted.")
    st.write("- Avatar updates based on detected emotion.")
    st.write("- Replies will include saved name if present.")

# ---------------------------------------------
# Helper: 4-second recorder
# ---------------------------------------------
def record_4_seconds(duration=4, sample_rate=16000, channels=1):
    st.info("Recording for 4 seconds... speak now.")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype="float32")
    sd.wait()
    # unique filename
    filename = "ui_sample.wav"
    filepath = os.path.join(AUDIO_DIR, filename)
    sf.write(filepath, recording, sample_rate)
    return os.path.abspath(filepath)

# ---------------------------------------------
# Main action
# ---------------------------------------------
if record_btn:
    try:
        filepath = record_4_seconds()
    except Exception as e:
        st.error(f"Recording failed: {e}")
        raise

    status_box.info("Analyzing your voice...")
    # Predict using absolute path (avoid relpath issues)
    try:
        emotion, probs = predict_emotion(filepath, model_path=MODEL_PATH)
    except Exception as e:
        st.error(f"Prediction error: {e}")
        raise

    if emotion is None:
        status_box.error("Could not detect emotion.")
    else:
        # update avatar (use fallback if missing)
        avatar_path = AVATAR_MAP.get(emotion, FALLBACK_AVATAR)
        avatar_placeholder.image(avatar_path, width=320)

        # show detected emotion & probs
        status_box.success(f"Detected Emotion: **{emotion.capitalize()}**")
        probs_box.write(probs)

        # generate reply and personalize with saved name if present
        reply = get_response(emotion)
        saved_name = get_name()
        if saved_name:
            # polite personalization: "Name, rest-of-sentence"
            if reply and reply[0].isalpha():
                reply = f"{saved_name}, {reply[0].lower()}{reply[1:]}"
            else:
                reply = f"{saved_name}, {reply}"

        # display and speak (speaking runs in main thread; it's okay)
        st.markdown("**Assistant reply:**")
        st.write(reply)

        try:
            speak(reply)
        except Exception as e:
            st.error(f"TTS playback failed: {e}")

# ---------------------------------------------
# Footer (small)
# ---------------------------------------------
st.markdown("---")
st.write("Tip: change or clear your saved name using the fields on the left.")



# streamlit run src/streamlit_app.py