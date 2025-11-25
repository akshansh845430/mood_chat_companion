# Mood Companion – Emotion-Based Voice Interaction App

A Streamlit + TensorFlow application that:
- records user voice (browser-based)
- extracts MFCC features
- predicts emotion (happy, sad, angry, neutral)
- displays emotion-specific animated avatars
- personalizes replies using user name memory
- speaks replies using neural TTS (edge-tts)

## Features
- 🎙 Browser-based voice recording (no sounddevice needed)
- 🤖 Custom-trained RAVDESS audio emotion model (LSTM)
- 🧠 Personalized responses with name memory
- 🎭 Animated GIF avatars based on emotion
- 🔊 Edge-TTS neural voice output
- 🌐 Fully deployable on Render

## Tech Stack
- Python, TensorFlow, Keras
- Librosa (MFCC extraction)
- Streamlit (UI)
- audio-recorder-streamlit (browser audio)
- edge-tts (text-to-speech)
- Soundfile, FFmpeg
- Render Cloud Hosting

## Deployment
1. Push this repo to GitHub.
2. Create a new Render Web Service.
3. Connect your repository.
4. Render auto-detects render.yaml.
5. Deployment finishes automatically.

## Local development
