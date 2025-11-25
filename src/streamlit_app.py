# src/streamlit_app.py

import streamlit as st
import os
import numpy as np
import soundfile as sf
from audio_recorder_streamlit import audio_recorder

from models.predict import predict_emotion
from utils.emotion_responder import get_response
from utils.tts_engine import speak
from utils.user_name_memory import get_name, set_name, FILE as NAME_FILE


# ------------------------------
# CONFIG
# ------------------------------
st.set_page_config(page_title="Mood Companion", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "..", "data", "audio_samples")
MODEL_PATH = os.path.join(BASE_DIR, "models", "emotion_model.h5")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(AUDIO_DIR, exist_ok=True)

# Avatar paths
AVATAR_MAP = {
    "neutral": os.path.join(ASSETS_DIR, "avatar_neutral.gif"),
    "happy": os.path.join(ASSETS_DIR, "avatar_happy.gif"),
    "sad": os.path.join(ASSETS_DIR, "avatar_sad.gif"),
    "angry": os.path.join(ASSETS_DIR, "avatar_angry.gif"),
}


# ------------------------------
# HEADER
# ------------------------------
st.markdown(
    "<h1 style='text-align:center; color:#f3a742;'>Your Mood Companion</h1>",
    unsafe_allow_html=True
)

avatar_placeholder = st.empty()
avatar_placeholder.image(AVATAR_MAP["neutral"], width=300)

status_box = st.empty()
reply_box = st.empty()


# ------------------------------
# NAME SETTINGS
# ------------------------------
st.markdown("---")
st.subheader("Your Name (optional)")

stored_name = get_name()
name_input = st.text_input("Name", value=stored_name or "")

colA, colB = st.columns(2)
with colA:
    if st.button("Save Name"):
        if name_input.strip():
            set_name(name_input.strip())
            st.success(f"Saved: {name_input.strip()}")
with colB:
    if st.button("Forget Name"):
        try:
            if os.path.exists(NAME_FILE):
                os.remove(NAME_FILE)
            st.success("Name removed.")
        except:
            pass


# ------------------------------
# RECORD (browser-based)
# ------------------------------
st.markdown("---")
st.subheader("🎙 Voice Input")

st.write("Click the button below and speak. Works on phone + cloud.")

audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#f3a742",
    neutral_color="#cccccc",
    icon_size="3x",
)

if audio_bytes:
    st.success("Recorded successfully!")

    # save audio to wav
    filepath = os.path.join(AUDIO_DIR, "ui_sample.wav")
    with open(filepath, "wb") as f:
        f.write(audio_bytes)

    # librosa needs wav → convert raw bytes to proper audio file
    audio_data, samplerate = sf.read(filepath)
    sf.write(filepath, audio_data, samplerate)

    status_box.info("Analyzing your voice...")

    # predict emotion
    emotion, probs = predict_emotion(filepath, model_path=MODEL_PATH)

    if emotion is None:
        status_box.error("Could not detect emotion.")
    else:
        avatar_placeholder.image(AVATAR_MAP.get(emotion, AVATAR_MAP["neutral"]), width=300)

        status_box.success(f"Detected Emotion: **{emotion.capitalize()}**")

        # generate response
        reply = get_response(emotion)

        # personalize
        saved_name = get_name()
        if saved_name:
            reply = f"{saved_name}, {reply[0].lower()}{reply[1:]}"

        reply_box.markdown(f"### 💬 Assistant: {reply}")

        # speak
        try:
            speak(reply)
        except Exception as e:
            st.error(f"TTS Error: {e}")
