from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from agentic_ppt_builder.state import AgentState, SlideContent

from agentic_ppt_builder.utils.logger import get_logger
from agentic_ppt_builder.utils.config import Config

logger = get_logger(__name__)

class SlideContentOutput(BaseModel):
    title: str = Field(description="Title of the slide")
    content: str = Field(description="Bullet points or detailed text for the slide")

class WriterOutput(BaseModel):
    slides: List[SlideContentOutput] = Field(description="List of fully written slides")

def writer_agent(state: AgentState):
    logger.info("--- WRITER AGENT STARTED ---")
    outline = state.get('presentation_outline', [])
    depth = state.get('depth', "Concise")

    if not outline:
        logger.warning("No outline provided to Writer Agent.")
        return {"slide_content": []}

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
        
        # Convert to internal state format (add missing fields)
        final_slides = []
        for s in slides:
            final_slides.append({
                "title": s['title'],
                "content": s['content'],
                "image_keyword": None,
                "image_url": None
            })

        return {"slide_content": final_slides}

    except Exception as e:

        logger.error(f"Writer Agent Error: {e}", exc_info=True)
        return {"slide_content": []}
