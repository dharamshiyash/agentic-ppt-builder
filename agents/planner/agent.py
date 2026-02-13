from state import AgentState
from agents.planner.service import generate_outline_service
from utils.logger import get_logger
from utils.config import Config

logger = get_logger(__name__)

def planner_agent(state: AgentState):
    """
    Planner Agent Node.
    Role: Converts topic → slide outline.
    Does NOT generate content or images.
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
