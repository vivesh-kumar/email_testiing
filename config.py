import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")

class Config:
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp19.mycloudmailbox.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "True").strip().lower() in ("true", "1", "yes")
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SENDER_NAME: str = os.getenv("SENDER_NAME", "B3 Communications")
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", os.getenv("SMTP_USERNAME", "B3Communications@b3intelligence.com"))
