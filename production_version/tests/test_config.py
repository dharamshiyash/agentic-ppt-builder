"""
Tests for Configuration
------------------------
Tests the Config class settings, defaults, and validation methods.
"""

import pytest
from config.settings import Config


class TestConfig:
    """Tests for the Config class."""

    def test_default_slide_count(self):
        """Default slide count should be 7."""
        assert Config.DEFAULT_SLIDE_COUNT == 7

    def test_max_slide_count(self):
        """Max slide count should be 20."""
        assert Config.MAX_SLIDE_COUNT == 20

    def test_min_slide_count(self):
        """Min slide count should be 1."""
        assert Config.MIN_SLIDE_COUNT == 1

    def test_max_topic_length(self):
        """Max topic length should be 200."""
        assert Config.MAX_TOPIC_LENGTH == 200

    def test_min_topic_length(self):
        """Min topic length should be 3."""
        assert Config.MIN_TOPIC_LENGTH == 3

    def test_allowed_fonts(self):
        """Should have at least 4 allowed fonts."""
        assert len(Config.ALLOWED_FONTS) >= 4
        assert "Arial" in Config.ALLOWED_FONTS
        assert "Calibri" in Config.ALLOWED_FONTS

    def test_allowed_depths(self):
        """Should have exactly 3 allowed depths."""
        assert Config.ALLOWED_DEPTHS == ["Minimal", "Concise", "Detailed"]

    def test_to_dict_redacts_api_keys(self):
        """to_dict should redact sensitive information."""
        config_dict = Config.to_dict()
        for key, value in config_dict.items():
            if "key" in key.lower() or "api" in key.lower():
                if value:
                    assert "***" in str(value) or value == "" or len(str(value)) <= 8

    def test_to_dict_includes_settings(self):
        """to_dict should include key configuration values."""
        config_dict = Config.to_dict()
        assert "OUTPUT_DIR" in config_dict
        assert "LOG_LEVEL" in config_dict

    def test_app_version_exists(self):
        """App version should be a non-empty string."""
        assert Config.APP_VERSION
        assert isinstance(Config.APP_VERSION, str)

    def test_output_dir_default(self):
        """Output dir should default to 'outputs'."""
        assert Config.OUTPUT_DIR == "outputs"
