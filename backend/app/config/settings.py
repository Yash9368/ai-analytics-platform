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

    # --- Anthropic (Claude AI) ---
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # --- CORS ---
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")


# ============================================
# Singleton settings instance
# ============================================
settings = Settings()
