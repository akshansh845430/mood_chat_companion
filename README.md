# Mood Companion – Voice Emotion Recognition Web App

Mood Companion is an AI-powered emotional assistant that:
- Listens to 4 seconds of your voice (browser recording)
- Predicts your emotion (Happy, Sad, Angry, Neutral)
- Responds with personalized, human-like speech using neural TTS
- Displays an animated avatar for each emotion
- Saves your name for personal replies

Built with: TensorFlow, Librosa, Streamlit, Edge-TTS, Python

---

## 🚀 Features

### 🎙 Voice Input (Browser)
Uses `audio_recorder_streamlit` — works on phone, laptop, and browser.

### 🧠 Emotion Detection
Custom-trained LSTM model on MFCC features.

### 🗣 AI Voice Reply
Neural voice using `edge-tts`.

### 😄 Animated Emotion Avatars
Shows GIF avatars depending on detected emotion.

### 🧑 Personalized Replies
If user saves a name, AI replies with it.

---

## 📂 Project Structure

