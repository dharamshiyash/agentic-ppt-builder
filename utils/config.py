import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Centralized configuration management for the application.
    Loads environment variables and sets default values.
    """

    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Used for DALL-E image generation (optional)

    # Application Settings
    LLM_MODEL = "llama-3.3-70b-versatile"  # scalable model
    DEFAULT_SLIDE_COUNT = 7
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    # Validation
    @classmethod
    def validate_keys(cls):
        """
        Checks if essential API keys are present.
        GROQ_API_KEY is required. Others trigger warnings if missing.
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

# Ensure output directory exists on startup
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
