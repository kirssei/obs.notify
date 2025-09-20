import os
from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = ["*"]

include("components/apps.py")

include("components/twitch.py")

include("components/channels.py")

include("components/database.py")

include("components/auth.py")

include("components/international.py")

include("components/static.py")