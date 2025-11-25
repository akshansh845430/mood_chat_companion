"""
voice_companion.py
Flow:
  1) Ask for name once (if not already saved)
  2) Record audio until ENTER is pressed (using your existing recorder)
  3) Feed the recorded .wav into your emotion model
  4) Generate an emotion-based reply
  5) Personalize reply with name if available
  6) Speak that reply using your TTS engine (edge-tts)
"""

import os
from models.predict import predict_emotion
from utils.emotion_responder import get_response
from utils.user_name_memory import set_name, get_name
from utils.tts_engine import speak   # neural TTS (edge-tts)
import audio_recording as ar

def personalize_reply(reply: str, user_name: str) -> str:
    """Insert user_name into reply naturally where sensible."""
    if not user_name:
        return reply

    # Simple, safe personalization rules
    # Prefer injecting after common starters
    starters = [
        ("I hear", f"I hear you, {user_name}"),
        ("You sound", f"You sound, {user_name},"),
        ("I'm here", f"I'm here for you, {user_name}"),
        ("There", f"{user_name}, there"),
    ]

    for prefix, replacement in starters:
        if reply.startswith(prefix):
            return reply.replace(prefix, replacement, 1)

    # fallback: prepend name politely
    # keep capitalization sensible
    if reply and reply[0].isalpha():
        return f"{user_name}, {reply[0].lower()}{reply[1:]}"
    return f"{user_name}, {reply}"

def ask_and_save_name_if_missing():
    name = get_name()
    if name:
        return name

    # Ask user for a preferred name once
    print("Before we begin — what should I call you? (press Enter to skip)")
    typed = input().strip()
    if typed:
        set_name(typed)
        print(f"Nice to meet you, {typed}!\n")
        return typed
    return None

def main():
    # Ensure working directory is src when running the script
    cwd = os.getcwd()
    src_dir = os.path.abspath(os.path.dirname(__file__))

    # Ask for name if not present
    user_name = ask_and_save_name_if_missing()

    print("\n🎙 Press ENTER to start recording...")
    input()
    print("🎤 Recording... Press ENTER again to stop.\n")

    # 1) RECORD AUDIO (your existing recorder handles saving)
    recorded_path = ar.record_audio()

    if not recorded_path or not os.path.exists(recorded_path):
        print("❌ Recording failed or file not found.")
        return

    print("\n📁 Recorded file:", recorded_path)

    # Convert to path relative to src for predict()
    audio_path_rel = os.path.relpath(recorded_path, start=src_dir)

    # 2) PREDICT EMOTION
    print("\n🔍 Predicting emotion...")
    emotion, probs = predict_emotion(audio_path_rel, model_path="models/emotion_model.h5")

    if emotion is None:
        print("Prediction failed.")
        return

    print("\n----------------------------")
    print("Detected Emotion:", emotion)
    print("Probabilities:", probs)
    print("----------------------------")

    # 3) GENERATE TEXT REPLY
    reply = get_response(emotion)

    # 4) PERSONALIZE if name exists
    if not user_name:
        user_name = get_name()  # maybe user set it in another run
    personalized = personalize_reply(reply, user_name)

    print("\n💬 AI Reply:", personalized)

    # 5) SPEAK REPLY (NEURAL VOICE)
    print("\n🔊 Speaking reply...\n")
    speak(personalized)

if __name__ == "__main__":
    main()
