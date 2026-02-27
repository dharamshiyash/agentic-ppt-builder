"""
Tests for utils/error_handler.py
"""
import pytest
from utils.error_handler import safe_run, with_retry, handle_agent_error


class TestSafeRun:
    def test_returns_result_on_success(self):
        result = safe_run(lambda: 42, fallback=0)
        assert result == 42

    def test_returns_fallback_on_exception(self):
        result = safe_run(lambda: 1 / 0, fallback="default", error_msg="Division by zero")
        assert result == "default"

    def test_returns_list_fallback(self):
        result = safe_run(lambda: (_ for _ in ()).throw(RuntimeError("fail")), fallback=[])
        assert result == []

    def test_error_msg_is_logged(self, caplog):
        import logging
        with caplog.at_level(logging.WARNING):
            safe_run(lambda: 1 / 0, fallback=None, error_msg="custom error message")
        assert "custom error message" in caplog.text


class TestWithRetry:
    def test_succeeds_on_first_attempt(self):
        call_count = {"n": 0}

        @with_retry(retries=3, delay=0)
        def func():
            call_count["n"] += 1
            return "ok"

        assert func() == "ok"
        assert call_count["n"] == 1

    def test_retries_and_eventually_succeeds(self):
        call_count = {"n": 0}

        @with_retry(retries=3, delay=0)
        def func():
            call_count["n"] += 1
            if call_count["n"] < 3:
                raise ValueError("not yet")
            return "success"

        assert func() == "success"
        assert call_count["n"] == 3

    def test_raises_after_exhausting_retries(self):
        @with_retry(retries=2, delay=0)
        def always_fails():
            raise RuntimeError("always fails")

        with pytest.raises(RuntimeError, match="always fails"):
            always_fails()


class TestHandleAgentError:
    def test_returns_fallback_state(self):
        exc = ValueError("test error")
        fallback = {"slide_content": [], "final_ppt_path": ""}
        result = handle_agent_error("TestAgent", exc, fallback)
        assert result == fallback

    def test_logs_error(self, caplog):
        import logging
        exc = RuntimeError("boom")
        with caplog.at_level(logging.ERROR):
            handle_agent_error("MyAgent", exc, {})
        assert "MyAgent" in caplog.text
        assert "boom" in caplog.text
