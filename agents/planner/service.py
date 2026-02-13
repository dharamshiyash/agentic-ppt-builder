from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser

from agents.planner.schema import PlannerOutput, ValidSlide
from utils.logger import get_logger
from utils.config import Config
from tools.cache import disk_cache
from tools.retry import api_retry

logger = get_logger(__name__)

@disk_cache
@api_retry
def generate_outline_service(topic: str, count: int, depth: str):
    """
    Core logic to generate a presentation outline using LLM.
    Uses caching and automatic retries for resilience.
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
        outline = response.get('outline', response) if isinstance(response, dict) else response
        logger.info(f"Successfully generated {len(outline)} slides.")
        return outline

    except Exception as e:
        logger.error(f"Planner Service Error: {e}", exc_info=True)
        # Return structured error fallback
        return [
            {"title": "Error", "description": "Failed to generate outline due to an internal error."}
        ]
