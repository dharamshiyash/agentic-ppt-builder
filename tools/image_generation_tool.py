"""
Tool 2: Image Generation / Fetching Tool
-----------------------------------------
Primary: DALL-E image generation (requires OPENAI_API_KEY).
Fallback: Unsplash stock photo lookup (requires UNSPLASH_ACCESS_KEY).
Second fallback: Placeholder dummy image URL (no keys needed).

Provides a unified interface: generate_or_fetch_image(prompt) -> str (URL)
"""
import requests
from utils.logger import get_logger
from utils.config import Config
from utils.error_handler import safe_run

logger = get_logger(__name__)

_DUMMY_URL = "https://dummyimage.com/600x400/cccccc/000000&text={query}"


def _generate_dalle_image(prompt: str) -> str:
    """Generate an image using OpenAI DALL-E 3."""
    from openai import OpenAI
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
    )
    url = response.data[0].url
    logger.info(f"DALL-E generated image for prompt: '{prompt[:50]}...'")
    return url


def _fetch_unsplash_image(query: str) -> str:
    """Fetch a royalty-free stock photo URL from Unsplash."""
    api_key = Config.UNSPLASH_ACCESS_KEY
    if not api_key:
        logger.warning("No Unsplash API key — skipping Unsplash.")
        return ""

    url = f"https://api.unsplash.com/search/photos?page=1&query={query}&client_id={api_key}"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            img_url = data["results"][0]["urls"]["regular"]
            logger.info(f"Unsplash image fetched for '{query}': {img_url}")
            return img_url
    logger.warning(f"Unsplash returned no results for '{query}'.")
    return ""


def generate_or_fetch_image(prompt: str) -> str:
    """
    Generate or fetch an image for a given prompt/keyword.

    Strategy (priority order):
      1. DALL-E 3 image generation (if OPENAI_API_KEY is set)
      2. Unsplash photo search (if UNSPLASH_ACCESS_KEY is set)
      3. Placeholder dummy image URL (always available)

    Args:
        prompt: The image description or search keyword.

    Returns:
        A URL string pointing to the image. Never raises an exception.
    """
    # Try DALL-E first
    if Config.OPENAI_API_KEY:
        url = safe_run(
            lambda: _generate_dalle_image(prompt),
            fallback="",
            error_msg=f"DALL-E generation failed for '{prompt}'. Trying Unsplash."
        )
        if url:
            return url

    # Try Unsplash fallback
    url = safe_run(
        lambda: _fetch_unsplash_image(prompt),
        fallback="",
        error_msg=f"Unsplash fetch failed for '{prompt}'. Using placeholder."
    )
    if url:
        return url

    # Final fallback — placeholder
    query_encoded = prompt.replace(" ", "+")
    placeholder = _DUMMY_URL.format(query=query_encoded)
    logger.warning(f"Using placeholder image for '{prompt}'.")
    return placeholder
