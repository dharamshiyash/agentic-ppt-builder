import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
    
    # Models
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
    
    # Defaults
    DEFAULT_SLIDE_COUNT = 7
    MAX_SLIDE_COUNT = 20
    MIN_SLIDE_COUNT = 1
    
    @classmethod
    def validate_keys(cls):
        """Check for critical API keys."""
        missing = []
        if not cls.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
        # Unsplash is optional but recommended for images
        if not cls.UNSPLASH_ACCESS_KEY:
             # Just a warning log might be appropriate in the caller
             pass
        return missing

# Ensure output directory exists
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
