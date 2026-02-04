from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from agentic_ppt_builder.state import AgentState, SlideContent

class SlideContentOutput(BaseModel):
    title: str = Field(description="Title of the slide")
    content: str = Field(description="Bullet points or detailed text for the slide")

class WriterOutput(BaseModel):
    slides: List[SlideContentOutput] = Field(description="List of fully written slides")

def writer_agent(state: AgentState):
    print("--- WRITER AGENT ---")
    outline = state['presentation_outline']
    depth = state['depth']

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
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
        print(f"Writer Agent Error: {e}")
        return {"slide_content": []}
