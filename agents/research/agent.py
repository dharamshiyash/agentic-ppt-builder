"""
Research Agent
--------------
Responsibilities:
- Takes the slide outline produced by PlannerAgent.
- Uses web_search_tool to collect factual data for each slide topic.
- Returns research_notes dict in AgentState for WriterAgent to use.

Does NOT:
- Generate slide text.
- Fetch images.
- Build PPT files.

Input: AgentState (presentation_outline)
Output: AgentState (research_notes)
"""
from state import AgentState
from agents.research.service import research_slides_service
from utils.logger import get_logger
from utils.error_handler import handle_agent_error

logger = get_logger(__name__)


def research_agent(state: AgentState):
    logger.info("--- RESEARCH AGENT STARTED ---")

    outline = state.get("presentation_outline", [])

    if not outline:
        logger.warning("ResearchAgent: No outline provided — skipping web research.")
        return {"research_notes": {}}

    try:
        notes = research_slides_service(outline)
        logger.info(f"ResearchAgent: Completed research for {len(notes)} slides.")
        return {"research_notes": notes}
    except Exception as exc:
        return handle_agent_error(
            agent_name="ResearchAgent",
            exc=exc,
            fallback_state={"research_notes": {}},
        )
