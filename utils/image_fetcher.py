import requests
import os
from agentic_ppt_builder.utils.config import Config
from agentic_ppt_builder.utils.logger import get_logger

logger = get_logger(__name__)

UNSPLASH_ACCESS_KEY = Config.UNSPLASH_ACCESS_KEY

def fetch_image_url(query: str) -> str:
    """
    Fetches an image URL from Unsplash based on the query.
    Returns a placeholder image if API fails or no key provided.
    """
    if not UNSPLASH_ACCESS_KEY:
        return f"https://dummyimage.com/600x400/cccccc/000000&text={query.replace(' ', '+')}"

    url = f"https://api.unsplash.com/search/photos?page=1&query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['urls']['regular']
    except Exception as e:
        logger.error(f"Error fetching image: {e}")

    return f"https://dummyimage.com/600x400/cccccc/000000&text={query.replace(' ', '+')}"
