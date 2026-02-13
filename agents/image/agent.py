from state import AgentState
from agents.image.service import fetch_image_url, generate_image_keyword
from utils.logger import get_logger

logger = get_logger(__name__)

def image_agent(state: AgentState):
    """
    Image Agent
    -----------
    Responsibilities:
    - Analyze slide content to determine visual needs.
    - Generate search keywords.
    - Fetch relevant royalty-free images via Unsplash API.
    
    Does NOT:
    - Modify slide text.
    - Change slide structure.
    - Create images from scratch (uses stock).
    
    Input: AgentState (slide_content)
    Output: AgentState (slide_content with image_url)
    """
    logger.info("--- IMAGE AGENT STARTED ---")
    
    slides = state.get('slide_content', [])
    
    if not slides:
        logger.warning("No slides to process in Image Agent.")
        return {"slide_content": []}
    
    updated_slides = []
    
    for slide in slides:
        try:
            # Generate Keyword
            keyword = generate_image_keyword(slide['title'], slide['content'])
            logger.info(f"Generated Keyword for '{slide['title']}': {keyword}")
            
            # Fetch Image
            url = fetch_image_url(keyword)
            
            # Update Slide
            new_slide = slide.copy()
            new_slide['image_keyword'] = keyword
            new_slide['image_url'] = url
            updated_slides.append(new_slide)
            
        except Exception as e:
            logger.error(f"Image Agent Error for slide {slide.get('title')}: {e}", exc_info=True)
            updated_slides.append(slide)

    return {"slide_content": updated_slides}
