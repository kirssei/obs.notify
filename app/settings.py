import os
from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = ["*"]

COMPONENTS = [
    "components/apps.py",
    "components/twitch.py",
    "components/channels.py",
    "components/database.py",
    "components/auth.py",
    "components/international.py",
    "components/static.py",
]

for conf in COMPONENTS:
    include(conf)
