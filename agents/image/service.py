import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from utils.logger import get_logger
from utils.config import Config
from tools.cache import disk_cache

logger = get_logger(__name__)

@disk_cache
def fetch_image_url(query: str) -> str:
    """
    Fetches an image URL from Unsplash based on the query.
    Returns a placeholder image if API fails or no key provided.
    Cached to prevent duplicate expensive calls.
    """
    api_key = Config.UNSPLASH_ACCESS_KEY
    if not api_key:
        logger.warning(f"No Unsplash API Key found. Returning placeholder for '{query}'.")
        return f"https://dummyimage.com/600x400/cccccc/000000&text={query.replace(' ', '+')}"

    url = f"https://api.unsplash.com/search/photos?page=1&query={query}&client_id={api_key}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                image_url = data['results'][0]['urls']['regular']
                logger.info(f"Fetched image for '{query}': {image_url}")
                return image_url
            else:
                logger.warning(f"No results found for '{query}'.")
        else:
             logger.warning(f"Unsplash API Error: {response.status_code} - {response.text}")
             
    except Exception as e:
        logger.error(f"Error fetching image: {e}")

    # Fallback
    return f"https://dummyimage.com/600x400/cccccc/000000&text={query.replace(' ', '+')}"

@disk_cache
def generate_image_keyword(title: str, content: str) -> str:
    """
    Uses LLM to generate a search keyword for the slide.
    Cached.
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
        return title # Fallback to title
