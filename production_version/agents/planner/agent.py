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
from utils.error_handler import handle_agent_error, LLMError
from config.settings import Config

logger = get_logger(__name__)


def planner_agent(state: AgentState) -> dict:
    """
    Generate a presentation outline from the topic using the LLM.

    Reads ``topic``, ``slide_count``, and ``depth`` from the shared state,
    calls the planner service, and returns the generated outline.
    Any LLM or service failure is caught and logged; an empty outline is
    returned so the pipeline can continue gracefully.

    Args:
        state (AgentState): The current shared agent state dict.

    Returns:
        dict: Partial state update with ``presentation_outline`` key.
            Returns empty list on failure.
    """
    logger.info("--- PLANNER AGENT STARTED ---")

    topic = state.get("topic", "")
    count = state.get("slide_count", Config.DEFAULT_SLIDE_COUNT)
    depth = state.get("depth", "Concise")

    if not topic:
        logger.error("No topic provided to PlannerAgent.")
        return {"presentation_outline": []}

    try:
        outline = generate_outline_service(topic, count, depth)
        logger.info(f"PlannerAgent completed: {len(outline)} slides outlined.")
        return {"presentation_outline": outline}
    except LLMError as e:
        logger.error(f"PlannerAgent LLM failure: {e}", exc_info=True)
        return {"presentation_outline": []}
    except Exception as e:
        return handle_agent_error(
            agent_name="PlannerAgent",
            exc=e,
            fallback_state={"presentation_outline": []},
        )
