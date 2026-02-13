from state import AgentState
from agents.builder.service import create_presentation_service
from utils.logger import get_logger
from utils.config import Config
import os

logger = get_logger(__name__)

def builder_agent(state: AgentState):
    """
    Builder Agent
    -------------
    Responsibilities:
    - Take final structured slide data.
    - Render text and images into a `.pptx` file.
    - Handle layout, fonts, and formatting.
    
    Does NOT:
    - Generate or modify content.
    - Fetch images or data.
    
    Input: AgentState (slide_content, topic, font)
    Output: AgentState (final_ppt_path)
    """
    logger.info("--- PPT BUILDER AGENT STARTED ---")
    
    slides = state.get('slide_content', [])
    font = state.get('font', "Calibri")
    
    if not slides:
        logger.warning("No slides provided to PPT Builder.")
        return {"final_ppt_path": ""}

    # Define output path
    output_dir = Config.OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{state.get('topic', 'Presentation').replace(' ', '_')}_presentation.pptx"
    output_path = os.path.join(output_dir, filename)
    
    final_path = create_presentation_service(slides, font_name=font, output_path=output_path)
    
    if not final_path:
        logger.error("Failed to generte PPT file.")
        return {"final_ppt_path": ""}
        
    return {"final_ppt_path": final_path}
