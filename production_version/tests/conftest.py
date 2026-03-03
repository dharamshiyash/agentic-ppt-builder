"""
Test configuration and shared fixtures.
"""

import os
import sys
import pytest
from unittest.mock import MagicMock

# Add production_version to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from core.state import AgentState


@pytest.fixture
def mock_agent_state():
    """Provide a standard AgentState dict for testing."""
    return {
        "topic": "Test Topic",
        "slide_count": 3,
        "font": "Arial",
        "depth": "Concise",
        "presentation_outline": [],
        "research_notes": {},
        "slide_content": [],
        "final_ppt_path": "",
    }


@pytest.fixture
def mock_outline():
    """Provide a sample presentation outline for testing."""
    return [
        {"title": "Introduction", "description": "Overview of the topic"},
        {"title": "Key Concepts", "description": "Core ideas explained"},
        {"title": "Conclusion", "description": "Summary and takeaways"},
    ]


@pytest.fixture
def mock_slides():
    """Provide sample slide content data for testing."""
    return [
        {
            "title": "Introduction",
            "content": "- Point 1\n- Point 2\n- Point 3",
            "image_keyword": "introduction",
            "image_url": "http://example.com/img1.jpg",
        },
        {
            "title": "Key Concepts",
            "content": "- Concept A\n- Concept B",
            "image_keyword": "concepts",
            "image_url": "http://example.com/img2.jpg",
        },
    ]


@pytest.fixture
def mock_slides_no_images():
    """Provide sample slides without images for testing."""
    return [
        {
            "title": "Slide 1",
            "content": "Content for slide 1",
            "image_keyword": None,
            "image_url": None,
        },
    ]
