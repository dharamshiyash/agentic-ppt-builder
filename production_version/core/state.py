"""
Agent State Definitions
-----------------------
Defines the shared state schema (TypedDict) that flows through the
LangGraph multi-agent pipeline. Every agent reads from and writes to
specific keys in this state.

State Flow:
    PlannerAgent  → sets presentation_outline
    ResearchAgent → sets research_notes
    WriterAgent   → sets slide_content
    ImageAgent    → updates slide_content with image_url / image_keyword
    BuilderAgent  → sets final_ppt_path
"""

from typing import List, Dict, TypedDict, Optional


class SlideContent(TypedDict):
    """Schema for a single slide's data after content generation."""

    title: str
    content: str  # Bullet points or text
    image_keyword: Optional[str]
    image_url: Optional[str]


class AgentState(TypedDict):
    """
    Shared state passed between all agents in the LangGraph pipeline.

    Attributes:
        topic: The user-provided presentation topic.
        slide_count: Number of slides to generate.
        font: Font name used throughout the presentation.
        depth: Content depth — one of "Minimal", "Concise", "Detailed".
        presentation_outline: List of slide outlines from PlannerAgent.
        research_notes: Per-slide web research snippets from ResearchAgent.
        slide_content: Fully written slide data from WriterAgent + ImageAgent.
        final_ppt_path: Absolute path to the generated .pptx file.
    """

    topic: str
    slide_count: int
    font: str
    depth: str
    presentation_outline: List[Dict[str, str]]
    research_notes: Optional[Dict[str, str]]
    slide_content: List[SlideContent]
    final_ppt_path: str
