
import pytest
from unittest.mock import MagicMock
from agentic_ppt_builder.state import AgentState

@pytest.fixture
def mock_agent_state():
    return {
        "topic": "Test Topic",
        "slide_count": 3,
        "font": "Arial",
        "depth": "Concise",
        "presentation_outline": [],
        "slide_content": [],
        "final_ppt_path": ""
    }

@pytest.fixture
def mock_outline():
    return [
        {"title": "Slide 1", "description": "Intro"},
        {"title": "Slide 2", "description": "Details"},
        {"title": "Slide 3", "description": "Conclusion"}
    ]

@pytest.fixture
def mock_slides():
    return [
        {
            "title": "Slide 1", 
            "content": "- Point 1\n- Point 2",
            "image_keyword": "test",
            "image_url": "http://example.com/img.jpg"
        },
        {
            "title": "Slide 2", 
            "content": "Detailed text content.",
            "image_keyword": "details",
            "image_url": "http://example.com/img2.jpg"
        }
    ]
