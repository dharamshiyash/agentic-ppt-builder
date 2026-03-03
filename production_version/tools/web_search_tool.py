"""
Web Search Tool
---------------
Provides web search capability to agents using DuckDuckGo (no API key required).
Falls back to empty results with a warning if the search fails.
"""

from typing import List
from utils.logger import get_logger
from utils.error_handler import safe_run

logger = get_logger(__name__)


def web_search(query: str, max_results: int = 5) -> List[str]:
    """
    Search the web using DuckDuckGo and return a list of text snippets.

    Uses the ``ddgs`` library (DuckDuckGo Search) which does not require
    an API key. If the search fails for any reason, returns an empty list
    so the pipeline can continue with LLM-only knowledge.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default: 5).

    Returns:
        list[str]: Text snippets relevant to the query. Empty on failure.
    """
    def _do_search():
        from ddgs import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                snippet = r.get("body", "") or r.get("snippet", "")
                if snippet:
                    results.append(snippet)
        logger.info(f"Web search for '{query}' returned {len(results)} results.")
        return results

    return safe_run(
        _do_search,
        fallback=[],
        error_msg=f"Web search failed for query: '{query}'. Falling back to LLM knowledge only."
    )


def web_search_formatted(query: str, max_results: int = 5) -> str:
    """
    Search the web and return results as a formatted string block.

    Convenient for injecting directly into LLM prompt context.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default: 5).

    Returns:
        str: A newline-separated string of search results prefixed with ``-``,
            or empty string if no results found.
    """
    results = web_search(query, max_results=max_results)
    if not results:
        return ""
    return "\n".join(f"- {r}" for r in results)
