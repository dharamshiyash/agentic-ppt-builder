"""
Tests for Planner Agent
------------------------
Tests the planner agent's outline generation, empty topic handling,
and error fallback behavior.
"""

import pytest
from unittest.mock import patch, MagicMock
from agents.planner.agent import planner_agent


class TestPlannerAgent:
    """Tests for the planner_agent function."""

    def test_empty_topic_returns_empty_outline(self, mock_agent_state):
        """Planner should return empty outline when no topic is provided."""
        mock_agent_state["topic"] = ""
        result = planner_agent(mock_agent_state)
        assert result["presentation_outline"] == []

    def test_none_topic_returns_empty_outline(self, mock_agent_state):
        """Planner should handle None topic gracefully."""
        mock_agent_state["topic"] = None
        result = planner_agent(mock_agent_state)
        assert result["presentation_outline"] == []

    @patch("agents.planner.agent.generate_outline_service")
    def test_successful_outline_generation(self, mock_service, mock_agent_state):
        """Planner should return outline from the service."""
        expected = [
            {"title": "Slide 1", "description": "Intro"},
            {"title": "Slide 2", "description": "Details"},
        ]
        mock_service.return_value = expected
        mock_agent_state["topic"] = "AI in Healthcare"

        result = planner_agent(mock_agent_state)

        assert result["presentation_outline"] == expected
        mock_service.assert_called_once_with("AI in Healthcare", 3, "Concise")

    @patch("agents.planner.agent.generate_outline_service")
    def test_uses_default_values(self, mock_service, mock_agent_state):
        """Planner should use defaults for missing state keys."""
        mock_service.return_value = []
        # Remove optional keys
        del mock_agent_state["slide_count"]
        del mock_agent_state["depth"]
        mock_agent_state["topic"] = "Test"

        planner_agent(mock_agent_state)

        # Should use Config defaults
        mock_service.assert_called_once()
        call_args = mock_service.call_args
        assert call_args[0][2] == "Concise"  # default depth
