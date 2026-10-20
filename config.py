import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")

class Config:
    # Mail Server (supports both MAIL_* and SMTP_* naming conventions)
    SMTP_SERVER: str = os.getenv("MAIL_SERVER") or os.getenv("SMTP_SERVER", "smtp19.mycloudmailbox.com")
    SMTP_PORT: int = int(os.getenv("MAIL_PORT") or os.getenv("SMTP_PORT", 587))
    SMTP_USE_TLS: bool = (os.getenv("MAIL_USE_TLS") or os.getenv("SMTP_USE_TLS", "True")).strip().lower() in ("true", "1", "yes")
    SMTP_USERNAME: str = os.getenv("MAIL_USERNAME") or os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("MAIL_PASSWORD") or os.getenv("SMTP_PASSWORD", "")
    SENDER_NAME: str = os.getenv("SENDER_NAME", "B3 Communications")
    SENDER_EMAIL: str = os.getenv("MAIL_DEFAULT_SENDER") or os.getenv("SENDER_EMAIL") or os.getenv("MAIL_USERNAME") or os.getenv("SMTP_USERNAME", "B3Communications@b3intelligence.com")

    # Security & Application Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "jwt_secret_key")
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH", 16777216))  # 16 MB
