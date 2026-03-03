"""
Application Settings
--------------------
Centralized configuration management for the Agentic PPT Builder.
All settings are loaded from environment variables with sensible defaults.

Environment Variables:
    GROQ_API_KEY        (required): API key for Groq LLM service.
    UNSPLASH_ACCESS_KEY (optional): API key for Unsplash image fetching.
    OPENAI_API_KEY      (optional): API key for DALL-E image generation.
    OUTPUT_DIR          (optional): Directory for generated PPTX files (default: outputs).
    LOG_LEVEL           (optional): Logging level (default: INFO).
    LOG_DIR             (optional): Directory for log files (default: logs).
    APP_VERSION         (optional): Application version string (default: 1.0.0).
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Centralized configuration management for the application.
    Loads environment variables and sets default values.

    All API keys and settings are accessed as class attributes.
    Call ``Config.validate_keys()`` at startup to verify required keys.
    """

    # ── API Keys ──────────────────────────────────────────────────────
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    UNSPLASH_ACCESS_KEY: str = os.getenv("UNSPLASH_ACCESS_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # ── Application Settings ─────────────────────────────────────────
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    DEFAULT_SLIDE_COUNT: int = 7
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "outputs")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    # ── Validation Constants ─────────────────────────────────────────
    MAX_TOPIC_LENGTH: int = 200
    MIN_TOPIC_LENGTH: int = 3
    MAX_SLIDE_COUNT: int = 20
    MIN_SLIDE_COUNT: int = 1
    ALLOWED_FONTS: list = ["Arial", "Calibri", "Times New Roman", "Consolas"]
    ALLOWED_DEPTHS: list = ["Minimal", "Concise", "Detailed"]

    # ── Timeout Settings ─────────────────────────────────────────────
    LLM_TIMEOUT: int = 60  # seconds
    IMAGE_FETCH_TIMEOUT: int = 10  # seconds
    WEB_SEARCH_TIMEOUT: int = 10  # seconds

    @classmethod
    def validate_keys(cls) -> None:
        """
        Validate that essential API keys are present.

        Raises:
            ValueError: If GROQ_API_KEY is missing (required for LLM calls).

        Warns (via logging):
            If UNSPLASH_ACCESS_KEY or OPENAI_API_KEY are missing.
        """
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is missing. Please set it in your .env file. "
                "Get your key at https://console.groq.com/"
            )
        if not cls.UNSPLASH_ACCESS_KEY:
            import logging
            logging.getLogger(__name__).warning(
                "UNSPLASH_ACCESS_KEY not set — image sourcing will use placeholder images. "
                "Get your key at https://unsplash.com/developers"
            )
        if not cls.OPENAI_API_KEY:
            import logging
            logging.getLogger(__name__).warning(
                "OPENAI_API_KEY not set — DALL-E image generation unavailable. "
                "Will fall back to Unsplash/placeholder images."
            )

    @classmethod
    def to_dict(cls) -> dict:
        """
        Return a sanitized dictionary of current configuration (redacts API keys).

        Returns:
            dict: Configuration key-value pairs with API keys masked.
        """
        return {
            "GROQ_API_KEY": "***SET***" if cls.GROQ_API_KEY else "NOT SET",
            "UNSPLASH_ACCESS_KEY": "***SET***" if cls.UNSPLASH_ACCESS_KEY else "NOT SET",
            "OPENAI_API_KEY": "***SET***" if cls.OPENAI_API_KEY else "NOT SET",
            "LLM_MODEL": cls.LLM_MODEL,
            "DEFAULT_SLIDE_COUNT": cls.DEFAULT_SLIDE_COUNT,
            "OUTPUT_DIR": cls.OUTPUT_DIR,
            "LOG_LEVEL": cls.LOG_LEVEL,
            "APP_VERSION": cls.APP_VERSION,
        }


# Ensure output and log directories exist on startup
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
os.makedirs(Config.LOG_DIR, exist_ok=True)
