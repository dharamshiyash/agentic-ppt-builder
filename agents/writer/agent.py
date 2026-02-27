from state import AgentState
from agents.writer.service import write_content_service
from utils.logger import get_logger

logger = get_logger(__name__)

def writer_agent(state: AgentState):
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

    Input: AgentState (presentation_outline, depth, research_notes)
    Output: AgentState (slide_content)
    """
    logger.info("--- WRITER AGENT STARTED ---")

    outline = state.get('presentation_outline', [])
    depth = state.get('depth', "Concise")
    research_notes = state.get('research_notes', {}) or {}

    if not outline:
        logger.warning("No outline provided to Writer Agent.")
        return {"slide_content": []}

    slides = write_content_service(outline, depth, research_notes)

    return {"slide_content": slides}
