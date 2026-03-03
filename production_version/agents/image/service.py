"""
Image Service
-------------
Handles image fetching from Unsplash and keyword generation via LLM.
Provides fallback to placeholder images when APIs are unavailable.
"""

import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from utils.logger import get_logger
from config.settings import Config
from tools.cache import disk_cache
from tools.retry import api_retry

logger = get_logger(__name__)


@disk_cache
@api_retry
def fetch_image_url(query: str) -> str:
    """
    Fetch an image URL from Unsplash based on the search query.

    Falls back to a placeholder image if:
        - No Unsplash API key is configured
        - The API returns no results
        - The API call fails

    Results are cached to disk and retried on transient failures.

    Args:
        query: The search keyword for finding a relevant image.

    Returns:
        str: A URL pointing to the image (Unsplash regular or placeholder).
    """
    api_key = Config.UNSPLASH_ACCESS_KEY
    if not api_key:
        logger.warning(f"No Unsplash API Key found. Returning placeholder for '{query}'.")
        return f"https://dummyimage.com/600x400/cccccc/000000&text={query.replace(' ', '+')}"

    url = f"https://api.unsplash.com/search/photos?page=1&query={query}&client_id={api_key}"

    try:
        response = requests.get(url, timeout=Config.IMAGE_FETCH_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                image_url = data["results"][0]["urls"]["regular"]
                logger.info(f"Fetched image for '{query}': {image_url}")
                return image_url
            else:
                logger.warning(f"No Unsplash results found for '{query}'.")
        else:
            logger.warning(f"Unsplash API Error: {response.status_code} - {response.text}")

    except requests.Timeout:
        logger.error(f"Unsplash API timeout for query '{query}'.")
    except Exception as e:
        logger.error(f"Error fetching image: {e}")

    # Fallback to placeholder
    return f"https://dummyimage.com/600x400/cccccc/000000&text={query.replace(' ', '+')}"


@disk_cache
@api_retry
def generate_image_keyword(title: str, content: str) -> str:
    """
    Use the LLM to generate an image search keyword from slide data.

    Args:
        title: The slide title.
        content: The slide content text.

    Returns:
        str: A 2-3 word search keyword. Falls back to the title on error.
    """
    llm = ChatGroq(model=Config.LLM_MODEL, temperature=0.5)

    prompt = ChatPromptTemplate.from_template(
        """
        You are a visual design assistant.
        For the following slide, provide a SINGLE specific search keyword or short phrase (2-3 words) to find a relevant high-quality stock image.
        Return ONLY the keyword. No quotes.

        Slide Title: {title}
        Slide Content: {content}
        """
    )

    chain = prompt | llm | StrOutputParser()

    try:
        keyword = chain.invoke({"title": title, "content": content})
        return keyword.strip()
    except Exception as e:
        logger.error(f"Error generating keyword: {e}")
        return title  # Fallback to title
