# src/streamlit_app.py
import streamlit as st
import numpy as np
import soundfile as sf
import os
from audio_recorder_streamlit import audio_recorder

from models.predict import predict_emotion
from utils.emotion_responder import get_response
from utils.tts_engine import speak
from utils.user_name_memory import get_name, set_name, FILE as NAME_FILE

# ===============================
# PATHS
# ===============================
st.set_page_config(page_title="Mood Companion", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "..", "data", "audio_samples")
MODEL_PATH = os.path.join(BASE_DIR, "models", "emotion_model.h5")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(AUDIO_DIR, exist_ok=True)

# Fallback if GIF not found
FALLBACK_AVATAR = "/mnt/data/Screenshot 2025-11-25 091414.png"

AVATAR_MAP = {
    "neutral": os.path.join(ASSETS_DIR, "avatar_neutral.gif")
        if os.path.exists(os.path.join(ASSETS_DIR, "avatar_neutral.gif")) else FALLBACK_AVATAR,
    "happy": os.path.join(ASSETS_DIR, "avatar_happy.gif")
        if os.path.exists(os.path.join(ASSETS_DIR, "avatar_happy.gif")) else FALLBACK_AVATAR,
    "sad": os.path.join(ASSETS_DIR, "avatar_sad.gif")
        if os.path.exists(os.path.join(ASSETS_DIR, "avatar_sad.gif")) else FALLBACK_AVATAR,
    "angry": os.path.join(ASSETS_DIR, "avatar_angry.gif")
        if os.path.exists(os.path.join(ASSETS_DIR, "avatar_angry.gif")) else FALLBACK_AVATAR,
}

# ===============================
# TITLE
# ===============================
st.markdown("<h1 style='text-align:center; color:#f3a742;'>Your Mood Companion</h1>", unsafe_allow_html=True)

# ===============================
# UI LAYOUT
# ===============================
col1, col2 = st.columns(2)

with col1:
    avatar_placeholder = st.empty()
    avatar_placeholder.image(AVATAR_MAP["neutral"], width=320)
    emotion_box = st.empty()
    probs_box = st.empty()

    st.markdown("---")
    st.write("Saved name (optional):")

    stored_name = get_name()
    name_input = st.text_input("Your name", value=stored_name or "")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Save"):
            if name_input.strip():
                set_name(name_input.strip())
                st.success(f"Saved name: {name_input.strip()}")
            else:
                st.warning("Enter a valid name.")

    with c2:
        if st.button("Forget"):
            if os.path.exists(NAME_FILE):
                os.remove(NAME_FILE)
            st.success("Name forgotten.")

with col2:
    st.write("🎙 Click below to record (browser mic):")
    audio_bytes = audio_recorder(text="Record your voice", recording_color="#ff4f4f", neutral_color="#6aa84f")

# ===============================
# PROCESS RECORDED AUDIO
# ===============================
if audio_bytes:
    st.info("Processing your voice...")

    file_path = os.path.join(AUDIO_DIR, "ui_sample.wav")
    with open(file_path, "wb") as f:
        f.write(audio_bytes)

    # Predict emotion
    emotion, probs = predict_emotion(file_path, model_path=MODEL_PATH)

    if emotion:
        avatar_placeholder.image(AVATAR_MAP.get(emotion, FALLBACK_AVATAR), width=320)

        emotion_box.success(f"Detected Emotion: **{emotion.capitalize()}**")
        probs_box.write(probs)

        # Response + personalization
        reply = get_response(emotion)
        user = get_name()

        if user:
            reply = f"{user}, {reply[0].lower()}{reply[1:]}" if reply else reply

        st.markdown("### 💬 Assistant:")
        st.write(reply)

        # Speak reply
        speak(reply)
    else:
        st.error("Could not detect emotion. Try again.")
