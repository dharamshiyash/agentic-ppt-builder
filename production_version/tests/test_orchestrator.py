"""
Tests for Agent Orchestrator
------------------------------
Tests the pipeline orchestration logic including input validation
integration, error handling, and pipeline execution flow.
"""

import pytest
from unittest.mock import patch, MagicMock
from services.orchestrator import run_pipeline
from utils.validators import ValidationError


class TestRunPipeline:
    """Tests for the run_pipeline orchestrator function."""

    def test_empty_topic_raises_validation_error(self):
        """Pipeline should reject empty topics."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            run_pipeline(topic="")

    def test_short_topic_raises_validation_error(self):
        """Pipeline should reject topics shorter than 3 characters."""
        with pytest.raises(ValidationError, match="at least"):
            run_pipeline(topic="AI")

    def test_long_topic_raises_validation_error(self):
        """Pipeline should reject topics longer than 200 characters."""
        with pytest.raises(ValidationError):
            run_pipeline(topic="A" * 201)

    def test_invalid_font_raises_validation_error(self):
        """Pipeline should reject unsupported fonts."""
        with pytest.raises(ValidationError, match="not supported"):
            run_pipeline(topic="Valid Topic", font="Comic Sans")

    def test_invalid_depth_raises_validation_error(self):
        """Pipeline should reject unsupported depth values."""
        with pytest.raises(ValidationError, match="not supported"):
            run_pipeline(topic="Valid Topic", depth="Super Detailed")

    def test_invalid_slide_count_raises(self):
        """Pipeline should reject out-of-range slide counts."""
        with pytest.raises(ValidationError, match="between"):
            run_pipeline(topic="Valid Topic", slide_count=100)

    @patch("core.graph.build_graph")
    def test_successful_pipeline(self, mock_build_graph):
        """Pipeline should invoke the graph and return final state."""
        mock_app = MagicMock()
        mock_app.invoke.return_value = {
            "topic": "Test",
            "final_ppt_path": "/output/test.pptx",
        }
        mock_build_graph.return_value = mock_app

        result = run_pipeline(topic="Test Topic", slide_count=3)

        assert result["final_ppt_path"] == "/output/test.pptx"
        mock_app.invoke.assert_called_once()

    @patch("core.graph.build_graph")
    def test_pipeline_no_ppt_generated(self, mock_build_graph):
        """Pipeline should handle cases where no PPT is generated."""
        mock_app = MagicMock()
        mock_app.invoke.return_value = {
            "topic": "Test",
            "final_ppt_path": "",
        }
        mock_build_graph.return_value = mock_app

        result = run_pipeline(topic="Test Topic")

        assert result["final_ppt_path"] == ""
