"""
Application Configuration

Loads environment variables using dotenv and exposes them
as a centralized Settings object via Pydantic BaseSettings.

Why Pydantic Settings?
- Type-safe configuration
- Automatic validation
- Environment variable loading
- Default values with override support
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================
# Load environment variables from .env file
# ============================================
# Walk up from config/ → app/ → backend/ to find .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """
    Centralized application settings.
    All values come from environment variables with sensible defaults.
    """

    # --- Server Settings ---
    APP_NAME: str = os.getenv("APP_NAME", "AI Analytics Platform")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # --- Frontend URL (for CORS) ---
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # --- Google Analytics ---
    GA4_PROPERTY_ID: str = os.getenv("GA4_PROPERTY_ID", "")
    GA4_CREDENTIALS_PATH: str = os.getenv(
        "GA4_CREDENTIALS_PATH",
        str(Path(__file__).resolve().parent.parent.parent / "credentials" / "ga4-service-account.json")
    )
    GA4_CREDENTIALS_JSON: str | None = os.getenv("GA4_CREDENTIALS_JSON", None)

    # --- Anthropic (Claude AI) ---
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # --- SMTP / Email Settings ---
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "")
    SMTP_FROM_NAME: str = os.getenv("SMTP_FROM_NAME", "AI Analytics Platform")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "")

    # --- CORS ---
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")


# ============================================
# Singleton settings instance
# ============================================
settings = Settings()

