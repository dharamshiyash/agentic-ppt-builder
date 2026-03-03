"""
Builder Agent
-------------
Responsibilities:
    - Take final structured slide data.
    - Render text and images into a ``.pptx`` file.
    - Handle layout, fonts, and formatting.

Does NOT:
    - Generate or modify content.
    - Fetch images or data.

Input:  AgentState (slide_content, topic, font)
Output: AgentState (final_ppt_path)
"""

from core.state import AgentState
from agents.builder.service import create_presentation_service
from utils.logger import get_logger
from config.settings import Config
import os

logger = get_logger(__name__)


def builder_agent(state: AgentState) -> dict:
    """
    Assemble the final .pptx file from structured slide data.

    Creates a PowerPoint presentation with title slide and content slides,
    applying the specified font and embedding fetched images.

    Args:
        state: The current AgentState dict.

    Returns:
        dict: Partial state update with ``final_ppt_path`` key.
            Empty string if no slides were provided or generation failed.
    """
    logger.info("--- PPT BUILDER AGENT STARTED ---")

    slides = state.get("slide_content", [])
    font = state.get("font", "Calibri")

    if not slides:
        logger.warning("No slides provided to BuilderAgent.")
        return {"final_ppt_path": ""}

    # Define output path
    output_dir = Config.OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{state.get('topic', 'Presentation').replace(' ', '_')}_presentation.pptx"
    output_path = os.path.join(output_dir, filename)

    final_path = create_presentation_service(slides, font_name=font, output_path=output_path)

    if not final_path:
        logger.error("Failed to generate PPT file.")
        return {"final_ppt_path": ""}

    logger.info(f"BuilderAgent completed: {final_path}")
    return {"final_ppt_path": final_path}
