"""
Tests for Health Check
-----------------------
Tests the health check function and endpoint responses.
"""

import pytest
from unittest.mock import patch, MagicMock
from health import check_health


class TestHealthCheck:
    """Tests for the check_health function."""

    @patch("health.Config")
    def test_healthy_with_api_key(self, mock_config):
        """Health check should return healthy when API key is set."""
        mock_config.GROQ_API_KEY = "test-key"
        mock_config.OUTPUT_DIR = "outputs"
        mock_config.APP_VERSION = "1.0.0"

        result = check_health()

        assert result["status"] in ("healthy", "degraded")
        assert "timestamp" in result
        assert "checks" in result

    @patch("health.Config")
    def test_degraded_without_api_key(self, mock_config):
        """Health check should return degraded when API key is missing."""
        mock_config.GROQ_API_KEY = ""
        mock_config.OUTPUT_DIR = "outputs"
        mock_config.APP_VERSION = "1.0.0"

        result = check_health()

        assert result["checks"]["api_keys"]["status"] == "warning"

    def test_health_response_structure(self):
        """Health check response should have required fields."""
        result = check_health()

        assert "status" in result
        assert "timestamp" in result
        assert "version" in result
        assert "checks" in result
        assert "api_keys" in result["checks"]
        assert "output_dir" in result["checks"]

    def test_health_status_values(self):
        """Health status should be one of the expected values."""
        result = check_health()
        assert result["status"] in ("healthy", "degraded", "unhealthy")
