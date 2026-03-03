"""
Planner Agent
-------------
Responsibilities:
    - Convert topic and slide count into a structured outline.
    - Plan the flow and narrative of the presentation.

Does NOT:
    - Generate full slide text.
    - Fetch images.
    - Build PPT files.

Input:  AgentState (topic, slide_count, depth)
Output: AgentState (presentation_outline)
"""

from core.state import AgentState
from agents.planner.service import generate_outline_service
from utils.logger import get_logger
from config.settings import Config

logger = get_logger(__name__)


def planner_agent(state: AgentState) -> dict:
    """
    Generate a presentation outline from the topic using the LLM.

    Reads ``topic``, ``slide_count``, and ``depth`` from the shared state,
    calls the planner service, and returns the generated outline.

    Args:
        state: The current AgentState dict.

    Returns:
        dict: Partial state update with ``presentation_outline`` key.
    """
    logger.info("--- PLANNER AGENT STARTED ---")

    topic = state.get("topic", "")
    count = state.get("slide_count", Config.DEFAULT_SLIDE_COUNT)
    depth = state.get("depth", "Concise")

    if not topic:
        logger.error("No topic provided to PlannerAgent.")
        return {"presentation_outline": []}

    outline = generate_outline_service(topic, count, depth)

    logger.info(f"PlannerAgent completed: {len(outline)} slides outlined.")
    return {"presentation_outline": outline}
