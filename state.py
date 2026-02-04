from typing import List, Dict, TypedDict, Optional

class SlideContent(TypedDict):
    title: str
    content: str  # Bullet points or text
    image_keyword: Optional[str]
    image_url: Optional[str]

class AgentState(TypedDict):
    topic: str
    slide_count: int
    font: str
    depth: str
    presentation_outline: List[Dict[str, str]] # List of {"title": "Slide Title", "description": "Brief description"}
    slide_content: List[SlideContent]        # Final content structure
    final_ppt_path: str
