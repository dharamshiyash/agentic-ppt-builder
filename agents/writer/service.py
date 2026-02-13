from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from typing import List, Dict, Any

from agents.writer.schema import WriterOutput, SlideContentOutput
from utils.logger import get_logger
from utils.config import Config
from tools.cache import disk_cache
from utils.resilience import api_retry

logger = get_logger(__name__)

@disk_cache
@api_retry
def write_content_service(outline: List[Dict[str, Any]], depth: str):
    """
    Core logic to write slide content.
    """
    logger.info("Writing content for slides...")
    
    llm = ChatGroq(model=Config.LLM_MODEL, temperature=0.7)
    parser = JsonOutputParser(pydantic_object=WriterOutput)

    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert content writer for presentations.
        Based on the provided outline, write the full content for each slide.
        Content Depth: "{depth}".
        
        Outline:
        {outline}

        For each slide, provide the 'title' (same as outline) and 'content' (formatted as bullet points using '-' or full text).
        Make sure the content is engaging, accurate, and suitable for a PowerPoint slide.
        
        {format_instructions}
        """
    )
    
    chain = prompt | llm | parser

    try:
        response = chain.invoke({
            "outline": str(outline),
            "depth": depth,
            "format_instructions": parser.get_format_instructions()
        })

        slides = response.get('slides', response) if isinstance(response, dict) else response
        
        # Convert to internal state format (add missing fields for next steps)
        final_slides = []
        for s in slides:
            final_slides.append({
                "title": s['title'],
                "content": s['content'],
                "image_keyword": None,
                "image_url": None
            })
            
        logger.info(f"Successfully wrote content for {len(final_slides)} slides.")
        return final_slides

    except Exception as e:
        logger.error(f"Writer Service Error: {e}", exc_info=True)
        return []
