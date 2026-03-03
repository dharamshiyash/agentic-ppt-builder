"""
Tests for Error Handler
------------------------
Tests safe_run, with_retry, handle_agent_error, and custom exceptions.
"""

import pytest
from unittest.mock import MagicMock, patch
from utils.error_handler import (
    safe_run,
    with_retry,
    handle_agent_error,
    LLMError,
    ImageFetchError,
    FileGenerationError,
    ConfigurationError,
    PipelineTimeoutError,
)


class TestSafeRun:
    """Tests for the safe_run utility."""

    def test_returns_result_on_success(self):
        """safe_run should return the function result on success."""
        result = safe_run(lambda: 42, fallback=0)
        assert result == 42

    def test_returns_fallback_on_exception(self):
        """safe_run should return fallback when function raises."""
        result = safe_run(lambda: 1 / 0, fallback=-1, error_msg="division error")
        assert result == -1

    def test_returns_fallback_on_runtime_error(self):
        """safe_run should catch RuntimeError and return fallback."""
        def failing():
            raise RuntimeError("test error")
        result = safe_run(failing, fallback="default")
        assert result == "default"

    def test_returns_list_fallback(self):
        """safe_run should handle list fallbacks correctly."""
        result = safe_run(lambda: [][0], fallback=[])
        assert result == []


class TestWithRetry:
    """Tests for the with_retry decorator."""

    def test_succeeds_first_try(self):
        """Decorated function should work normally when no error."""
        @with_retry(retries=3, delay=0.01)
        def succeed():
            return "ok"

        assert succeed() == "ok"

    def test_retries_then_succeeds(self):
        """Decorated function should retry and eventually succeed."""
        call_count = {"n": 0}

        @with_retry(retries=3, delay=0.01)
        def flaky():
            call_count["n"] += 1
            if call_count["n"] < 3:
                raise ValueError("not yet")
            return "ok"

        assert flaky() == "ok"
        assert call_count["n"] == 3

    def test_exhausts_retries_and_raises(self):
        """Decorated function should raise after exhausting retries."""
        @with_retry(retries=2, delay=0.01)
        def always_fail():
            raise ValueError("permanent failure")

        with pytest.raises(ValueError, match="permanent failure"):
            always_fail()


class TestHandleAgentError:
    """Tests for handle_agent_error."""

    def test_returns_fallback_state(self):
        """Should return the fallback state dict."""
        fallback = {"research_notes": {}}
        result = handle_agent_error("TestAgent", ValueError("test"), fallback)
        assert result == fallback

    def test_returns_empty_path_fallback(self):
        """Should handle path fallback correctly."""
        fallback = {"final_ppt_path": ""}
        result = handle_agent_error("BuilderAgent", RuntimeError("fail"), fallback)
        assert result["final_ppt_path"] == ""


class TestCustomExceptions:
    """Tests for custom exception classes."""

    def test_llm_error(self):
        with pytest.raises(LLMError):
            raise LLMError("API call failed")

    def test_image_fetch_error(self):
        with pytest.raises(ImageFetchError):
            raise ImageFetchError("Image not found")

    def test_file_generation_error(self):
        with pytest.raises(FileGenerationError):
            raise FileGenerationError("Cannot save file")

    def test_configuration_error(self):
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Missing API key")

    def test_pipeline_timeout_error(self):
        with pytest.raises(PipelineTimeoutError):
            raise PipelineTimeoutError("Timeout exceeded")

    def test_exceptions_are_subclass_of_exception(self):
        """All custom exceptions should inherit from Exception."""
        for exc_class in [LLMError, ImageFetchError, FileGenerationError,
                          ConfigurationError, PipelineTimeoutError]:
            assert issubclass(exc_class, Exception)
