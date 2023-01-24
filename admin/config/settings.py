import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

APP_NAME = os.environ.get("APP_NAME")

DEBUG = os.environ.get("DEBUG", False)

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(" ")

include(
    "components/application_definition.py",
    "components/database.py",
    "components/password_validation.py",
    "components/internationalization.py",
)

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOCALE_PATH = ["locale"]

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE")

TIME_ZONE = os.environ.get("TIME_ZONE")

PHONE_NUMBERS_REGION = os.environ.get("PHONE_NUMBERS_REGION")
