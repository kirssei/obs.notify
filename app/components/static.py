import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")