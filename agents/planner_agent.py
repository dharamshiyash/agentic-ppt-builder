from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from agentic_ppt_builder.state import AgentState

# Define Output Schema
class ValidSlide(BaseModel):
    title: str = Field(description="Title of the slide")
    description: str = Field(description="Brief instruction on what content should be on this slide")

class PlannerOutput(BaseModel):
    outline: List[ValidSlide] = Field(description="List of slides for the presentation")

def planner_agent(state: AgentState):
    print("--- PLANNER AGENT ---")
    topic = state['topic']
    count = state['slide_count']
    depth = state['depth']

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
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
        
        return {"presentation_outline": outline}

    except Exception as e:
        print(f"Planner Agent Error: {e}")
        # Fallback
        return {"presentation_outline": [{"title": "Error", "description": "Failed to generate outline"}]}
