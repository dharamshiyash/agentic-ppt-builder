from state import AgentState
from utils.ppt_utils import create_presentation
from utils.logger import get_logger
from utils.config import Config
import os

logger = get_logger(__name__)

def ppt_builder_agent(state: AgentState):
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
    
    try:
        final_path = create_presentation(slides, font_name=font, output_path=output_path)
        logger.info(f"Presentation saved to: {final_path}")
    except Exception as e:
        logger.error(f"PPT Builder failed: {e}", exc_info=True)
        return {"final_ppt_path": ""}
    
    return {"final_ppt_path": final_path}
