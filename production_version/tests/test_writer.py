"""
Tests for Writer Agent
-----------------------
Tests the writer agent's content generation, research note integration,
and empty outline handling.
"""

import pytest
from unittest.mock import patch, MagicMock
from agents.writer.agent import writer_agent


class TestWriterAgent:
    """Tests for the writer_agent function."""

    def test_empty_outline_returns_empty_slides(self, mock_agent_state):
        """Writer should return empty slides when no outline is provided."""
        mock_agent_state["presentation_outline"] = []
        result = writer_agent(mock_agent_state)
        assert result["slide_content"] == []

    @patch("agents.writer.agent.write_content_service")
    def test_successful_content_writing(self, mock_service, mock_agent_state):
        """Writer should return slides from the service."""
        expected_slides = [
            {"title": "Slide 1", "content": "Content 1", "image_keyword": None, "image_url": None},
        ]
        mock_service.return_value = expected_slides
        mock_agent_state["presentation_outline"] = [
            {"title": "Slide 1", "description": "Intro"},
        ]

        result = writer_agent(mock_agent_state)

        assert result["slide_content"] == expected_slides
        mock_service.assert_called_once()

    @patch("agents.writer.agent.write_content_service")
    def test_passes_research_notes(self, mock_service, mock_agent_state):
        """Writer should pass research notes to the service."""
        mock_service.return_value = []
        mock_agent_state["presentation_outline"] = [{"title": "Slide 1", "description": "Intro"}]
        mock_agent_state["research_notes"] = {"Slide 1": "- Fact 1\n- Fact 2"}

        writer_agent(mock_agent_state)

        call_args = mock_service.call_args
        assert call_args[0][2] == {"Slide 1": "- Fact 1\n- Fact 2"}

    @patch("agents.writer.agent.write_content_service")
    def test_handles_none_research_notes(self, mock_service, mock_agent_state):
        """Writer should handle None research notes gracefully."""
        mock_service.return_value = []
        mock_agent_state["presentation_outline"] = [{"title": "Slide 1", "description": "Intro"}]
        mock_agent_state["research_notes"] = None

        writer_agent(mock_agent_state)

        call_args = mock_service.call_args
        assert call_args[0][2] == {}
