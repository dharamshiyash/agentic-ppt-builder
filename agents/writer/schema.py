from typing import List
from pydantic import BaseModel, Field

class SlideContentOutput(BaseModel):
    title: str = Field(description="Title of the slide")
    content: str = Field(description="Bullet points or detailed text for the slide")

class WriterOutput(BaseModel):
    slides: List[SlideContentOutput] = Field(description="List of fully written slides")
