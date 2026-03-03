"""
Writer Service
--------------
Core logic for writing slide content using the Groq LLM.
Integrates research notes from the ResearchAgent to ground
content in factual data rather than relying solely on LLM training.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from typing import List, Dict, Any, Optional

from agents.writer.schema import WriterOutput, SlideContentOutput
from utils.logger import get_logger
from config.settings import Config
from tools.cache import disk_cache
from tools.retry import api_retry

logger = get_logger(__name__)


@disk_cache
@api_retry
def write_content_service(
    outline: List[Dict[str, Any]],
    depth: str,
    research_notes: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Write detailed slide content from the outline using LLM.

    Constructs a prompt that includes the outline and any available
    research notes, then invokes the LLM to generate full slide text.
    Results are cached to disk and retried on transient failures.

    Args:
        outline: List of slide dicts with ``title`` and ``description`` keys.
        depth: Content depth — "Minimal", "Concise", or "Detailed".
        research_notes: Optional dict mapping slide titles to fact strings.

    Returns:
        list[dict]: A list of slide dicts with ``title``, ``content``,
            ``image_keyword``, and ``image_url`` keys. Returns empty list on failure.
    """
    logger.info("Writing content for slides...")

    research_notes = research_notes or {}
    llm = ChatGroq(model=Config.LLM_MODEL, temperature=0.7)
    parser = JsonOutputParser(pydantic_object=WriterOutput)

    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert content writer for presentations.
        Based on the provided outline, write the full content for each slide.
        Content Depth: "{depth}".

        Outline:
        {outline}

        Additional Research Facts (use these to enrich the content where relevant):
        {research_context}

        For each slide, provide the 'title' (same as outline) and 'content' (formatted as bullet points using '-' or full text).
        Make sure the content is engaging, accurate, and suitable for a PowerPoint slide.

        {format_instructions}
        """
    )

    chain = prompt | llm | parser

    # Build research context string
    research_lines = []
    for title, facts in research_notes.items():
        if facts:
            research_lines.append(f"[{title}]\n{facts}")
    research_context = "\n\n".join(research_lines) if research_lines else "No additional research available."

    try:
        response = chain.invoke({
            "outline": str(outline),
            "depth": depth,
            "research_context": research_context,
            "format_instructions": parser.get_format_instructions()
        })

        slides = response.get("slides", response) if isinstance(response, dict) else response

        # Convert to internal state format (add missing fields for next steps)
        final_slides = []
        for s in slides:
            final_slides.append({
                "title": s["title"],
                "content": s["content"],
                "image_keyword": None,
                "image_url": None
            })

        logger.info(f"Successfully wrote content for {len(final_slides)} slides.")
        return final_slides

    except Exception as e:
        logger.error(f"Writer Service Error: {e}", exc_info=True)
        return []
