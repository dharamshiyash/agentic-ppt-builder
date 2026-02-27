"""
Tests for agents/research/agent.py and agents/research/service.py
"""
import pytest
from unittest.mock import patch


class TestResearchService:
    @patch("agents.research.service.web_search_formatted")
    def test_returns_notes_for_each_slide(self, mock_search):
        from agents.research.service import research_slides_service
        mock_search.return_value = "- Fact 1\n- Fact 2"

        outline = [
            {"title": "Intro", "description": "Introduction to AI"},
            {"title": "Impact", "description": "AI Impact on Society"},
        ]

        notes = research_slides_service(outline)
        assert "Intro" in notes
        assert "Impact" in notes
        assert notes["Intro"] == "- Fact 1\n- Fact 2"

    @patch("agents.research.service.web_search_formatted", return_value="")
    def test_empty_research_on_no_results(self, mock_search):
        from agents.research.service import research_slides_service
        outline = [{"title": "Topic", "description": "Desc"}]
        notes = research_slides_service(outline)
        assert notes["Topic"] == ""

    def test_empty_outline_returns_empty_dict(self):
        from agents.research.service import research_slides_service
        notes = research_slides_service([])
        assert notes == {}


class TestResearchAgent:
    @patch("agents.research.agent.research_slides_service")
    def test_agent_sets_research_notes(self, mock_service):
        from agents.research.agent import research_agent
        mock_service.return_value = {"Slide 1": "Fact A"}

        state = {
            "presentation_outline": [{"title": "Slide 1", "description": "desc"}],
        }

        result = research_agent(state)
        assert result == {"research_notes": {"Slide 1": "Fact A"}}

    def test_agent_handles_empty_outline(self):
        from agents.research.agent import research_agent
        state = {"presentation_outline": []}
        result = research_agent(state)
        assert result == {"research_notes": {}}

    @patch("agents.research.agent.research_slides_service", side_effect=RuntimeError("crash"))
    def test_agent_handles_exception(self, mock_service):
        from agents.research.agent import research_agent
        state = {"presentation_outline": [{"title": "T", "description": "D"}]}
        result = research_agent(state)
        assert result == {"research_notes": {}}
