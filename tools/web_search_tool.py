"""
Tool 1: Web Search Tool
-----------------------
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

    Args:
        query: The search query string.
        max_results: Maximum number of results to return.

    Returns:
        A list of text snippets relevant to the query.
        Returns an empty list if the search fails.
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
    Convenient for injecting into LLM prompts.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return.

    Returns:
        A newline-separated string of search results, or empty string on failure.
    """
    results = web_search(query, max_results=max_results)
    if not results:
        return ""
    return "\n".join(f"- {r}" for r in results)
