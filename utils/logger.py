import logging
import sys
from utils.config import Config

def get_logger(name: str):
    """
    Returns a configured logger instance with structured formatting.
    
    Args:
        name (str): The name of the logger (usually __name__).
    """
    logger = logging.getLogger(name)
    
    # Only configure if handlers haven't been set to avoid duplicate logs
    if not logger.handlers:
        logger.setLevel(Config.LOG_LEVEL)
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(Config.LOG_LEVEL)
        
        # Create formatter
        # JSON-like structure is often preferred for production, but readable text is fine for this scope.
        # We will use a clear readable format.
        formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger
