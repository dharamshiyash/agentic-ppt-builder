"""
Tests for PPT Builder Agent
-----------------------------
Tests the builder agent's presentation creation, file saving,
and error handling.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from agents.builder.agent import builder_agent


class TestBuilderAgent:
    """Tests for the builder_agent function."""

    def test_empty_slides_returns_empty_path(self, mock_agent_state):
        """Builder should return empty path when no slides are provided."""
        mock_agent_state["slide_content"] = []
        result = builder_agent(mock_agent_state)
        assert result["final_ppt_path"] == ""

    @patch("agents.builder.agent.create_presentation_service")
    def test_successful_build(self, mock_service, mock_agent_state, mock_slides):
        """Builder should return the path from the service."""
        mock_service.return_value = "/outputs/test.pptx"
        mock_agent_state["slide_content"] = mock_slides
        mock_agent_state["topic"] = "Test Topic"

        result = builder_agent(mock_agent_state)

        assert result["final_ppt_path"] == "/outputs/test.pptx"
        mock_service.assert_called_once()

    @patch("agents.builder.agent.create_presentation_service")
    def test_failed_build_returns_empty_path(self, mock_service, mock_agent_state, mock_slides):
        """Builder should return empty path when service returns empty."""
        mock_service.return_value = ""
        mock_agent_state["slide_content"] = mock_slides

        result = builder_agent(mock_agent_state)

        assert result["final_ppt_path"] == ""

    @patch("agents.builder.agent.create_presentation_service")
    def test_uses_correct_font(self, mock_service, mock_agent_state, mock_slides):
        """Builder should pass the font from state to the service."""
        mock_service.return_value = "/outputs/test.pptx"
        mock_agent_state["slide_content"] = mock_slides
        mock_agent_state["font"] = "Times New Roman"

        builder_agent(mock_agent_state)

        call_kwargs = mock_service.call_args
        assert call_kwargs[1]["font_name"] == "Times New Roman"

    @patch("agents.builder.service.Presentation")
    def test_create_presentation_service_creates_file(self, MockPresentation, mock_slides, tmp_path):
        """Service should create and save a PPTX file."""
        from agents.builder.service import create_presentation_service

        # Mock the Presentation object
        mock_prs = MagicMock()
        MockPresentation.return_value = mock_prs

        # Mock slide layouts
        mock_layout = MagicMock()
        mock_prs.slide_layouts.__getitem__ = MagicMock(return_value=mock_layout)

        # Mock slide
        mock_slide = MagicMock()
        mock_prs.slides.add_slide.return_value = mock_slide
        mock_slide.shapes.title = MagicMock()
        mock_slide.shapes.title.text_frame.paragraphs = []

        output_path = str(tmp_path / "test.pptx")
        result = create_presentation_service(mock_slides, output_path=output_path)

        mock_prs.save.assert_called_once_with(output_path)
