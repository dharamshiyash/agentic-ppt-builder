from typing import List
from pydantic import BaseModel, Field

class ValidSlide(BaseModel):
    title: str = Field(description="Title of the slide")
    description: str = Field(description="Brief instruction on what content should be on this slide")

class PlannerOutput(BaseModel):
    outline: List[ValidSlide] = Field(description="List of slides for the presentation")
