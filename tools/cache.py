import os
import pickle
import hashlib
from functools import wraps
from utils.logger import get_logger
from utils.config import Config

logger = get_logger(__name__)

CACHE_DIR = ".cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def disk_cache(func):
    """
    A simple decorator to cache function results to disk using pickle.
    Useful for expensive LLM calls or API requests to save time/cost.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create a unique cache key based on function name and arguments
        # We stringify args and kwargs to create a hash
        key_content = f"{func.__name__}:{str(args)}:{str(kwargs)}"
        cache_key = hashlib.md5(key_content.encode()).hexdigest()
        cache_file = os.path.join(CACHE_DIR, f"{cache_key}.pkl")
        
        # Check if cache exists
        if os.path.exists(cache_file):
            logger.debug(f"Cache hit for {func.__name__} (Key: {cache_key})")
            try:
                with open(cache_file, "rb") as f:
                    return pickle.load(f)
            except Exception as e:
                logger.warning(f"Failed to read cache: {e}. Re-executing function.")
        
        # Execute function
        result = func(*args, **kwargs)
        
        # Save to cache
        try:
            with open(cache_file, "wb") as f:
                pickle.dump(result, f)
            logger.debug(f"Cached result for {func.__name__} (Key: {cache_key})")
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
            
        return result
        
    return wrapper

def clear_cache():
    """Clears all cached files."""
    try:
        for filename in os.listdir(CACHE_DIR):
            file_path = os.path.join(CACHE_DIR, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        logger.info("Cache cleared successfully.")
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
