"""
Image Agent
-----------
Responsibilities:
    - Analyze slide content to determine visual needs.
    - Generate search keywords using LLM.
    - Fetch relevant royalty-free images via Unsplash API.

Does NOT:
    - Modify slide text.
    - Change slide structure.
    - Create images from scratch (uses stock, unless DALL-E is configured).

Input:  AgentState (slide_content)
Output: AgentState (slide_content with image_url and image_keyword)
"""

from core.state import AgentState
from agents.image.service import fetch_image_url, generate_image_keyword
from utils.logger import get_logger

logger = get_logger(__name__)


def image_agent(state: AgentState) -> dict:
    """
    Source images for each slide based on content analysis.

    For each slide, uses the LLM to generate a relevant search keyword,
    then fetches an image URL from Unsplash (or falls back to placeholder).

    Args:
        state: The current AgentState dict.

    Returns:
        dict: Partial state update with ``slide_content`` key,
            where each slide now includes ``image_keyword`` and ``image_url``.
    """
    logger.info("--- IMAGE AGENT STARTED ---")

    slides = state.get("slide_content", [])

    if not slides:
        logger.warning("No slides to process in ImageAgent.")
        return {"slide_content": []}

    updated_slides = []

    for slide in slides:
        try:
            # Generate keyword from slide content
            keyword = generate_image_keyword(slide["title"], slide["content"])
            logger.info(f"Generated keyword for '{slide['title']}': {keyword}")

            # Fetch image URL
            url = fetch_image_url(keyword)

            # Update slide with image data
            new_slide = slide.copy()
            new_slide["image_keyword"] = keyword
            new_slide["image_url"] = url
            updated_slides.append(new_slide)

        except Exception as e:
            logger.error(f"ImageAgent error for slide '{slide.get('title')}': {e}", exc_info=True)
            updated_slides.append(slide)

    logger.info(f"ImageAgent completed: {len(updated_slides)} slides processed.")
    return {"slide_content": updated_slides}
