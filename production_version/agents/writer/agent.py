"""
Writer Agent
------------
Responsibilities:
    - Convert structured outline into detailed slide content.
    - Generate bullet points and narrative text.
    - Incorporates factual research notes from ResearchAgent.

Does NOT:
    - Fetch images.
    - Build PPT files.
    - Change the outline structure.

Input:  AgentState (presentation_outline, depth, research_notes)
Output: AgentState (slide_content)
"""

from core.state import AgentState
from agents.writer.service import write_content_service
from utils.logger import get_logger

logger = get_logger(__name__)


def writer_agent(state: AgentState) -> dict:
    """
    Write detailed slide content from the outline and research notes.

    Reads the outline, depth preference, and optional research notes,
    then generates full slide content with titles and bullet points.

    Args:
        state: The current AgentState dict.

    Returns:
        dict: Partial state update with ``slide_content`` key.
    """
    logger.info("--- WRITER AGENT STARTED ---")

    outline = state.get("presentation_outline", [])
    depth = state.get("depth", "Concise")
    research_notes = state.get("research_notes", {}) or {}

    if not outline:
        logger.warning("No outline provided to WriterAgent.")
        return {"slide_content": []}

    slides = write_content_service(outline, depth, research_notes)

    logger.info(f"WriterAgent completed: {len(slides)} slides written.")
    return {"slide_content": slides}
