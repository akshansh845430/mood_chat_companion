# src/streamlit_app.py
"""
Deploy-ready Streamlit app for Mood Companion.

- Uses a browser-side recorder component (no sounddevice/soundfile).
- Keeps name personalization, avatar switching, emotion prediction, and TTS.
- Tries multiple recorder component imports for robustness.
"""

import os
import streamlit as st
from pathlib import Path

# app-specific imports (keep your existing code usage)
from models.predict import predict_emotion
from utils.emotion_responder import get_response
from utils.tts_engine import speak
from utils.user_name_memory import get_name, set_name, FILE as NAME_FILE

# Try several recorder components (community packages name differences)
AUDIO_RECORDER = None
RECORDER_NAME = None
try:
    # package: audio-recorder-streamlit  -> import audio_recorder
    from audio_recorder_streamlit import audio_recorder as audio_recorder_func  # type: ignore
    AUDIO_RECORDER = audio_recorder_func
    RECORDER_NAME = "audio_recorder_streamlit.audio_recorder"
except Exception:
    try:
        # package: streamlit-audiorecorder -> import audiorecorder
        from streamlit_audiorecorder import audiorecorder as audio_recorder_func2  # type: ignore
        AUDIO_RECORDER = audio_recorder_func2
        RECORDER_NAME = "streamlit_audiorecorder.audiorecorder"
    except Exception:
        try:
            # another variant name
            from streamlit_audiorecorder import audiorecorder  # type: ignore
            AUDIO_RECORDER = audiorecorder
            RECORDER_NAME = "streamlit_audiorecorder.audiorecorder"
        except Exception:
            AUDIO_RECORDER = None

# CONFIG & PATHS
st.set_page_config(page_title="Mood Companion", layout="centered")

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = (BASE_DIR / ".." / "data" / "audio_samples").resolve()
MODEL_PATH = (BASE_DIR / "models" / "emotion_model.h5").resolve()
ASSETS_DIR = (BASE_DIR / "assets").resolve()

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Fallback avatar (session file you uploaded earlier)
FALLBACK_AVATAR = "/mnt/data/Screenshot 2025-11-25 091414.png"

AVATAR_MAP = {
    "neutral": str(ASSETS_DIR / "avatar_neutral.gif") if (ASSETS_DIR / "avatar_neutral.gif").exists() else FALLBACK_AVATAR,
    "happy":   str(ASSETS_DIR / "avatar_happy.gif")   if (ASSETS_DIR / "avatar_happy.gif").exists()   else FALLBACK_AVATAR,
    "sad":     str(ASSETS_DIR / "avatar_sad.gif")     if (ASSETS_DIR / "avatar_sad.gif").exists()     else FALLBACK_AVATAR,
    "angry":   str(ASSETS_DIR / "avatar_angry.gif")   if (ASSETS_DIR / "avatar_angry.gif").exists()   else FALLBACK_AVATAR,
}

# UI header
st.markdown("<h1 style='text-align:center; color:#f3a742;'>Your Mood Companion</h1>", unsafe_allow_html=True)
st.write("")  # small spacing

# Layout: left = avatar + name, right = recorder + info
col_left, col_right = st.columns([1, 1])

with col_left:
    avatar_placeholder = st.empty()
    avatar_placeholder.image(AVATAR_MAP["neutral"], width=320)

    st.markdown("---")
    st.write("Saved name (optional):")
    stored_name = get_name()
    name_input = st.text_input("Your name", value=stored_name or "")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Save name"):
            if name_input.strip():
                set_name(name_input.strip())
                st.success(f"Saved name: {name_input.strip()}")
            else:
                st.warning("Please enter a non-empty name.")
    with c2:
        if st.button("Forget name"):
            try:
                if os.path.exists(NAME_FILE):
                    os.remove(NAME_FILE)
                st.success("Name forgotten.")
            except Exception as e:
                st.error(f"Could not forget name: {e}")

with col_right:
    st.write("🎙 Record (browser) — works on phone & cloud")
    st.write("Allow microphone access when prompted by your browser.")
    st.markdown("---")

status_box = st.empty()
probs_box = st.empty()
reply_box = st.empty()

# Recorder availability check
if AUDIO_RECORDER is None:
    st.warning(
        "No browser recorder component found. Install one of these in your environment:\n\n"
        "`pip install audio-recorder-streamlit`  OR  `pip install streamlit-audiorecorder`\n\n"
        "Then refresh this page."
    )
    st.stop()

# Show recorder UI and capture returned bytes (API differs slightly by package)
st.write(f"Using recorder: {RECORDER_NAME}" if RECORDER_NAME else "Using browser recorder")

# Call the recorder; both components usually return WAV bytes when recording stops.
# Parameters differ across packages; we'll call with minimal args and accept returned bytes-like.
audio_bytes = None
try:
    # audio_recorder from audio_recorder_streamlit uses (text, sample_rate=..., ...)
    if RECORDER_NAME and "audio_recorder_streamlit" in RECORDER_NAME:
        audio_bytes = AUDIO_RECORDER("Click to record/stop")
    else:
        # streamlit_audiorecorder's 'audiorecorder' returns bytes with same two-arg signature in many installs
        audio_bytes = AUDIO_RECORDER("Click to record/stop", "Recording...")
except TypeError:
    # try with single arg fallback
    try:
        audio_bytes = AUDIO_RECORDER("Click to record/stop")
    except Exception:
        audio_bytes = None
except Exception:
    audio_bytes = None

# Helper to persist bytes to a .wav file
def save_audio_bytes_to_wav(raw_bytes, out_path: Path) -> bool:
    if raw_bytes is None:
        return False
    try:
        # raw_bytes may be bytes, bytearray, memoryview or similar
        if isinstance(raw_bytes, (bytes, bytearray)):
            data = bytes(raw_bytes)
        elif hasattr(raw_bytes, "tobytes"):
            data = raw_bytes.tobytes()
        else:
            # attempt to convert
            data = bytes(raw_bytes)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        st.error(f"Failed saving audio: {e}")
        return False

# When audio is present, save and run pipeline
if audio_bytes:
    status_box.info("Saving and analyzing your voice...")
    wav_path = AUDIO_DIR / "ui_sample.wav"
    ok = save_audio_bytes_to_wav(audio_bytes, wav_path)
    if not ok:
        status_box.error("Failed to save audio. Try again.")
    else:
        # Run prediction (predict_emotion handles model loading)
        try:
            emotion, probs = predict_emotion(str(wav_path), model_path=str(MODEL_PATH))
        except Exception as e:
            emotion, probs = None, None
            status_box.error(f"Prediction error: {e}")

        if emotion is None:
            status_box.error("Could not detect emotion.")
        else:
            avatar_placeholder.image(AVATAR_MAP.get(emotion, FALLBACK_AVATAR), width=320)
            status_box.success(f"Detected Emotion: **{emotion.capitalize()}**")
            probs_box.write(probs)

            # build reply and personalize with stored name
            reply = get_response(emotion)
            user = get_name()
            if user:
                # polite personalization
                if reply and reply[0].isalpha():
                    reply = f"{user}, {reply[0].lower()}{reply[1:]}"
                else:
                    reply = f"{user}, {reply}"

            reply_box.markdown("### 💬 Assistant reply:")
            reply_box.write(reply)

            # Speak reply (your utils.tts_engine.speak should handle edge-tts or fallback)
            try:
                speak(reply)
            except Exception as e:
                st.error(f"TTS failed: {e}")

st.markdown("---")
st.write("Tip: Save a name to personalize replies. This UI uses browser recording (works on phone).")
