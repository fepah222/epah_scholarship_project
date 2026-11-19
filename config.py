import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-before-deployment")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///epah_scholarship.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = int(os.getenv("UPLOAD_MAX_MB", "8")) * 1024 * 1024
    UPLOAD_ROOT = BASE_DIR / "uploads"
    PUBLIC_UPLOAD = UPLOAD_ROOT / "public"
    PRIVATE_UPLOAD = UPLOAD_ROOT / "private"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
