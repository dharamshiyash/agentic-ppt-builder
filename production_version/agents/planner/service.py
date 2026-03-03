"""
Planner Service
---------------
Core logic for generating presentation outlines using the Groq LLM.
Uses caching and automatic retries for resilience.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser

from agents.planner.schema import PlannerOutput, ValidSlide
from utils.logger import get_logger
from config.settings import Config
from tools.cache import disk_cache
from tools.retry import api_retry

logger = get_logger(__name__)


@disk_cache
@api_retry
def generate_outline_service(topic: str, count: int, depth: str) -> list:
    """
    Generate a structured presentation outline using the LLM.

    Combines a prompt template with the Groq LLM and a JSON parser to
    produce a list of slide objects with ``title`` and ``description`` fields.

    Results are cached to disk and retried automatically on transient failures.

    Args:
        topic: The presentation topic string.
        count: Number of slides to generate.
        depth: Content depth — "Minimal", "Concise", or "Detailed".

    Returns:
        list[dict]: A list of dicts, each with ``title`` and ``description`` keys.
            On failure, returns a single-element list with an error slide.
    """
    logger.info(f"Generating outline for topic: '{topic}' with {count} slides.")

    llm = ChatGroq(model=Config.LLM_MODEL, temperature=0.7)
    parser = JsonOutputParser(pydantic_object=PlannerOutput)

    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert presentation planner.
        Create a slide outline for a presentation on the topic: "{topic}".
        The presentation should have exactly {count} slides.
        The content depth should be: "{depth}".

        Return a JSON list of slides, where each slide has a 'title' and a 'description'.
        
        {format_instructions}
        """
    )

    chain = prompt | llm | parser

    try:
        response = chain.invoke({
            "topic": topic,
            "count": count,
            "depth": depth,
            "format_instructions": parser.get_format_instructions()
        })

        # Normalize output if nested
        outline = response.get("outline", response) if isinstance(response, dict) else response
        logger.info(f"Successfully generated {len(outline)} slides.")
        return outline

    except Exception as e:
        logger.error(f"Planner Service Error: {e}", exc_info=True)
        return [
            {"title": "Error", "description": "Failed to generate outline due to an internal error."}
        ]
