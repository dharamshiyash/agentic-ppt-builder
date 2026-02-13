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
    
    # Application Settings
    LLM_MODEL = "llama-3.3-70b-versatile" # scalable model
    DEFAULT_SLIDE_COUNT = 7
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Validation
    @classmethod
    def validate_keys(cls):
        """Checks if essential API keys are present."""
        missing = []
        if not cls.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
        if not cls.UNSPLASH_ACCESS_KEY:
            missing.append("UNSPLASH_ACCESS_KEY")
            
        if missing:
            raise ValueError(f"Missing API Keys: {', '.join(missing)}. Please set them in your .env file.")

# Ensure output directory exists on startup
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
