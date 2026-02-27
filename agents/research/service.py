"""
Research Agent Service
-----------------------
Uses the web_search_tool to gather factual information about each slide topic.
Result is a dict: {slide_title: "fact1\nfact2\n..."}
"""
from typing import List, Dict, Any
from utils.logger import get_logger
from tools.web_search_tool import web_search_formatted

logger = get_logger(__name__)


def research_slides_service(outline: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    For each slide in the outline, perform a web search and collect
    relevant factual snippets.

    Args:
        outline: List of dicts with 'title' and 'description' keys.

    Returns:
        Dict mapping slide title → newline-separated fact strings.
        Empty string value if search returned no results for that slide.
    """
    research_notes: Dict[str, str] = {}

    for slide in outline:
        title = slide.get("title", "")
        description = slide.get("description", "")
        query = f"{title}: {description}".strip(": ")

        if not query:
            continue

        logger.info(f"ResearchAgent: Searching for '{query}'")
        facts = web_search_formatted(query, max_results=3)

        if facts:
            research_notes[title] = facts
            logger.info(f"ResearchAgent: Found {len(facts.splitlines())} snippets for '{title}'")
        else:
            logger.warning(f"ResearchAgent: No results for '{title}' — will rely on LLM knowledge.")
            research_notes[title] = ""

    return research_notes
