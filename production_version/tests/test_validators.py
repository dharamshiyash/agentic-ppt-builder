"""
Tests for Input Validation
---------------------------
Covers all validation functions in utils/validators.py including
edge cases, boundary conditions, and sanitization.
"""

import pytest
from utils.validators import (
    validate_topic,
    validate_slide_count,
    validate_font,
    validate_depth,
    validate_all_inputs,
    sanitize_input,
    ValidationError,
)


class TestSanitizeInput:
    """Tests for the sanitize_input function."""

    def test_strips_whitespace(self):
        assert sanitize_input("  hello  ") == "hello"

    def test_escapes_html(self):
        result = sanitize_input("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    def test_removes_control_characters(self):
        result = sanitize_input("hello\x00world\x07test")
        assert "\x00" not in result
        assert "\x07" not in result
        assert "helloworld" in result

    def test_collapses_multiple_spaces(self):
        assert sanitize_input("hello    world") == "hello world"

    def test_preserves_normal_text(self):
        assert sanitize_input("Normal text here") == "Normal text here"

    def test_handles_non_string(self):
        result = sanitize_input(123)
        assert result == "123"


class TestValidateTopic:
    """Tests for the validate_topic function."""

    def test_valid_topic(self):
        assert validate_topic("Artificial Intelligence") == "Artificial Intelligence"

    def test_empty_topic_raises(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_topic("")

    def test_none_topic_raises(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_topic(None)

    def test_whitespace_only_raises(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_topic("   ")

    def test_too_short_raises(self):
        with pytest.raises(ValidationError, match="at least"):
            validate_topic("AI")

    def test_too_long_raises(self):
        long_topic = "A" * 201
        with pytest.raises(ValidationError, match="at most"):
            validate_topic(long_topic)

    def test_exactly_min_length(self):
        result = validate_topic("abc")
        assert result == "abc"

    def test_exactly_max_length(self):
        topic = "A" * 200
        result = validate_topic(topic)
        assert len(result) == 200

    def test_strips_and_sanitizes(self):
        result = validate_topic("  Hello World  ")
        assert result == "Hello World"


class TestValidateSlideCount:
    """Tests for the validate_slide_count function."""

    def test_valid_count(self):
        assert validate_slide_count(5) == 5

    def test_none_returns_default(self):
        result = validate_slide_count(None)
        assert result == 7  # Config.DEFAULT_SLIDE_COUNT

    def test_min_boundary(self):
        assert validate_slide_count(1) == 1

    def test_max_boundary(self):
        assert validate_slide_count(20) == 20

    def test_below_min_raises(self):
        with pytest.raises(ValidationError, match="between"):
            validate_slide_count(0)

    def test_above_max_raises(self):
        with pytest.raises(ValidationError, match="between"):
            validate_slide_count(21)

    def test_string_number_converts(self):
        assert validate_slide_count("5") == 5

    def test_invalid_type_raises(self):
        with pytest.raises(ValidationError, match="integer"):
            validate_slide_count("abc")


class TestValidateFont:
    """Tests for the validate_font function."""

    def test_valid_font(self):
        assert validate_font("Arial") == "Arial"

    def test_none_returns_default(self):
        assert validate_font(None) == "Calibri"

    def test_empty_returns_default(self):
        assert validate_font("") == "Calibri"

    def test_invalid_font_raises(self):
        with pytest.raises(ValidationError, match="not supported"):
            validate_font("Comic Sans")

    def test_all_allowed_fonts(self):
        for font in ["Arial", "Calibri", "Times New Roman", "Consolas"]:
            assert validate_font(font) == font


class TestValidateDepth:
    """Tests for the validate_depth function."""

    def test_valid_depth(self):
        assert validate_depth("Concise") == "Concise"

    def test_none_returns_default(self):
        assert validate_depth(None) == "Concise"

    def test_empty_returns_default(self):
        assert validate_depth("") == "Concise"

    def test_invalid_depth_raises(self):
        with pytest.raises(ValidationError, match="not supported"):
            validate_depth("Very Detailed")

    def test_all_allowed_depths(self):
        for depth in ["Minimal", "Concise", "Detailed"]:
            assert validate_depth(depth) == depth


class TestValidateAllInputs:
    """Tests for the validate_all_inputs convenience function."""

    def test_all_valid(self):
        result = validate_all_inputs(
            topic="Machine Learning",
            slide_count=5,
            font="Arial",
            depth="Detailed",
        )
        assert result["topic"] == "Machine Learning"
        assert result["slide_count"] == 5
        assert result["font"] == "Arial"
        assert result["depth"] == "Detailed"

    def test_defaults_applied(self):
        result = validate_all_inputs(topic="AI Tech")
        assert result["slide_count"] == 7
        assert result["font"] == "Calibri"
        assert result["depth"] == "Concise"

    def test_invalid_topic_propagates(self):
        with pytest.raises(ValidationError):
            validate_all_inputs(topic="")

    def test_invalid_count_propagates(self):
        with pytest.raises(ValidationError):
            validate_all_inputs(topic="Valid Topic", slide_count=100)
