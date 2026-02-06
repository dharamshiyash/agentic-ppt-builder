import logging
import sys
import os

def get_logger(name: str) -> logging.Logger:
    """Configures and returns a logger instance."""
    
    logger = logging.getLogger(name)
    
    # If logger already has handlers, assume it's configured and return it
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger
