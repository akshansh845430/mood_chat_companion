import edge_tts
import asyncio
import os
from datetime import datetime
import pygame

VOICE_NAME = "en-US-AriaNeural"

async def _speak_async(text):
    # output path for audio
    output_file = os.path.join(
        os.path.dirname(__file__),
        f"tts_output_{datetime.now().strftime('%H%M%S')}.mp3"
    )

    communicate = edge_tts.Communicate(text, VOICE_NAME)
    await communicate.save(output_file)

    # Play using pygame (stable & smooth on Windows)
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    # Wait until playback finishes
    while pygame.mixer.music.get_busy():
        continue

def speak(text):
    try:
        asyncio.run(_speak_async(text))
    except RuntimeError:
        # Fix for "event loop already running"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_speak_async(text))
