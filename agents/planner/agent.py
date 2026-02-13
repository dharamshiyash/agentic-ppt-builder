from state import AgentState
from agents.planner.service import generate_outline_service
from utils.logger import get_logger
from utils.config import Config

logger = get_logger(__name__)

def planner_agent(state: AgentState):
    """
    Planner Agent
    -------------
    Responsibilities:
    - Convert topic and slide count into structured outline.
    - Plan the flow and narrative of the presentation.
    
    Does NOT:
    - Generate full slide text.
    - Fetch images.
    - Build PPT files.
    
    Input: AgentState (topic, slide_count, depth)
    Output: AgentState (presentation_outline)
    """
    logger.info("--- PLANNER AGENT STARTED ---")
    
    topic = state.get('topic', "")
    count = state.get('slide_count', Config.DEFAULT_SLIDE_COUNT)
    depth = state.get('depth', "Concise")

    if not topic:
        logger.error("No topic provided.")
        return {"presentation_outline": []}

    outline = generate_outline_service(topic, count, depth)
    
    return {"presentation_outline": outline}
