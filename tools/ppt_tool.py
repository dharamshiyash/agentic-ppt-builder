"""
Tool 3: PPT Generation Tool
-----------------------------
Named tool wrapper around agents/builder/service.py::create_presentation_service.
Provides the clean public API for PPT generation that ReadyTensor expects
to see as an explicit, named tool.
"""
import os
from typing import List, Dict, Any
from utils.logger import get_logger
from utils.config import Config
from utils.error_handler import safe_run

logger = get_logger(__name__)


def build_pptx(
    slides: List[Dict[str, Any]],
    font_name: str = "Calibri",
    output_path: str = None,
) -> str:
    """
    Build a PowerPoint (.pptx) file from structured slide data.

    Args:
        slides: List of slide dicts with keys:
                  - title (str): Slide title
                  - content (str): Bullet-point text (newline separated)
                  - image_url (str, optional): URL of the slide image
        font_name: Font to use throughout the presentation.
        output_path: Destination file path. Auto-generated if None.

    Returns:
        The file path of the saved .pptx, or empty string on failure.
    """
    from agents.builder.service import create_presentation_service

    if not slides:
        logger.warning("build_pptx called with no slides. Aborting.")
        return ""

    # Auto-generate output path if not provided
    if not output_path:
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        topic = slides[0].get("title", "Presentation").replace(" ", "_")
        output_path = os.path.join(Config.OUTPUT_DIR, f"{topic}_presentation.pptx")

    logger.info(f"PPT Tool: Building presentation → {output_path}")

    result = safe_run(
        lambda: create_presentation_service(slides, font_name=font_name, output_path=output_path),
        fallback="",
        error_msg=f"PPT generation failed for '{output_path}'."
    )

    if result:
        logger.info(f"PPT Tool: Presentation saved at {result}")
    else:
        logger.error("PPT Tool: build_pptx returned empty path.")

    return result
