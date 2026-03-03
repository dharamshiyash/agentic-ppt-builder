"""
Error Handler Utility
---------------------
Provides centralized error handling, custom exception classes, safe execution
wrappers, and fallback strategies for all agents and tools in the pipeline.

Custom Exceptions:
    LLMError             — LLM API call failures
    ImageFetchError      — Image retrieval failures
    FileGenerationError  — PPT file creation failures
    ConfigurationError   — Missing or invalid configuration
    PipelineTimeoutError — Pipeline execution timeout
"""

import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


# ── Custom Exception Classes ────────────────────────────────────────────


class LLMError(Exception):
    """Raised when an LLM API call fails after retries."""
    pass


class ImageFetchError(Exception):
    """Raised when image fetching or generation fails."""
    pass


class FileGenerationError(Exception):
    """Raised when PPT file creation or saving fails."""
    pass


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""
    pass


class PipelineTimeoutError(Exception):
    """Raised when the agent pipeline exceeds the allowed execution time."""
    pass


# ── Safe Execution Wrapper ──────────────────────────────────────────────


def safe_run(func: Callable, fallback: Any, error_msg: str = "", *args, **kwargs) -> Any:
    """
    Execute a callable safely with fallback on failure.

    If any exception is raised, log the error and return the fallback value
    instead of propagating the exception. This prevents individual failures
    from crashing the entire pipeline.

    Args:
        func: A zero-argument callable (use lambdas to capture arguments).
        fallback: The value to return if ``func`` raises any exception.
        error_msg: Human-readable context for the log message.

    Returns:
        The result of ``func()``, or ``fallback`` on any exception.

    Example:
        >>> result = safe_run(lambda: risky_api_call(x), fallback=[], error_msg="API failed")
    """
    try:
        return func()
    except Exception as exc:
        msg = error_msg or f"safe_run caught an error in {getattr(func, '__name__', str(func))}"
        logger.warning(f"{msg} | Exception: {type(exc).__name__}: {exc}")
        return fallback


# ── Retry Decorator ─────────────────────────────────────────────────────


def with_retry(retries: int = 3, delay: float = 2.0, backoff: float = 2.0):
    """
    Decorator factory: retry a function up to ``retries`` times with
    exponential backoff before raising the final exception.

    Args:
        retries: Maximum number of attempts (including the first).
        delay: Initial delay in seconds between attempts.
        backoff: Multiplier applied to delay after each failure.

    Returns:
        A decorator that wraps the target function with retry logic.

    Example:
        >>> @with_retry(retries=3, delay=1.0)
        ... def call_api():
        ...     ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            last_exc = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    retry_msg = f"Retrying in {wait:.1f}s..." if attempt < retries else "No more retries."
                    logger.warning(
                        f"[Retry {attempt}/{retries}] {func.__name__} failed: "
                        f"{type(exc).__name__}: {exc}. {retry_msg}"
                    )
                    if attempt < retries:
                        time.sleep(wait)
                        wait *= backoff
            raise last_exc  # Re-raise after exhausting retries
        return wrapper
    return decorator


# ── Agent Error Handler ─────────────────────────────────────────────────


def handle_agent_error(agent_name: str, exc: Exception, fallback_state: dict) -> dict:
    """
    Standardized error handler for LangGraph agent nodes.

    Logs the error with full traceback and returns a fallback partial state
    so the pipeline can continue rather than crash entirely.

    Args:
        agent_name: Name of the agent (for logging).
        exc: The caught exception.
        fallback_state: Dict of state keys/values to return on error.

    Returns:
        The ``fallback_state`` dict, allowing the pipeline to proceed.
    """
    logger.error(
        f"[{agent_name}] Unexpected error: {type(exc).__name__}: {exc}",
        exc_info=True,
    )
    return fallback_state
