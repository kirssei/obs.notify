import os
import uuid
from gtts import gTTS
from django.conf import settings


def generate_tts(text: str) -> str:
    tts_dir = os.path.join(settings.BASE_DIR, "static", "tts")
    os.makedirs(tts_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(tts_dir, filename)

    tts = gTTS(text=text, lang="ru")
    tts.save(filepath)

    return f"static/tts/{filename}"
