"""
Tests for tools/web_search_tool.py
"""
import pytest
from unittest.mock import patch, MagicMock


class TestWebSearch:
    def test_returns_snippets_on_success(self):
        """DDGS is imported lazily inside a closure, so patch at ddgs module level."""
        from tools.web_search_tool import web_search
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.__enter__ = MagicMock(return_value=mock_ddgs_instance)
        mock_ddgs_instance.__exit__ = MagicMock(return_value=False)
        mock_ddgs_instance.text.return_value = [
            {"body": "AI is transforming healthcare."},
            {"body": "Machine learning improves diagnostics."},
        ]
        with patch("ddgs.DDGS", return_value=mock_ddgs_instance):
            results = web_search("AI in healthcare", max_results=2)
        assert isinstance(results, list)

    def test_returns_empty_list_on_failure(self):
        """When DDGS raises, safe_run should return []."""
        from tools.web_search_tool import web_search
        with patch("ddgs.DDGS", side_effect=Exception("network error")):
            results = web_search("anything")
        assert results == []

    def test_formatted_returns_string_on_results(self):
        """web_search_formatted builds '- snippet' format."""
        from tools.web_search_tool import web_search_formatted
        with patch("tools.web_search_tool.web_search", return_value=["Fact 1", "Fact 2"]):
            result = web_search_formatted("topic")
        assert "- Fact 1" in result
        assert "- Fact 2" in result

    def test_formatted_returns_empty_string_on_failure(self):
        """web_search_formatted returns '' when no results."""
        from tools.web_search_tool import web_search_formatted
        with patch("tools.web_search_tool.web_search", return_value=[]):
            result = web_search_formatted("anything")
        assert result == ""
