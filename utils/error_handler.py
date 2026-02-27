"""
Error Handler Utility
---------------------
Provides centralized error handling, safe execution wrappers, and
fallback strategies for all agents and tools in the pipeline.
"""
import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def safe_run(func: Callable, fallback: Any, error_msg: str = "", *args, **kwargs) -> Any:
    """
    Execute a callable safely. If any exception is raised, log the error
    message and return the fallback value instead of propagating the exception.

    Args:
        func: A zero-argument callable (use lambdas to capture arguments).
        fallback: The value to return if func raises any exception.
        error_msg: Human-readable context for the log message.
        *args / **kwargs: Ignored (use closures/lambdas instead).

    Returns:
        The result of func(), or fallback on any exception.

    Example:
        result = safe_run(lambda: risky_api_call(x), fallback=[], error_msg="API failed")
    """
    try:
        return func()
    except Exception as exc:
        msg = error_msg or f"safe_run caught an error in {getattr(func, '__name__', str(func))}"
        logger.warning(f"{msg} | Exception: {type(exc).__name__}: {exc}")
        return fallback


def with_retry(retries: int = 3, delay: float = 2.0, backoff: float = 2.0):
    """
    Decorator factory: retry a function up to `retries` times with exponential
    backoff before raising the final exception.

    Args:
        retries: Maximum number of attempts (including the first).
        delay: Initial delay in seconds between attempts.
        backoff: Multiplier applied to delay after each failure.

    Example:
        @with_retry(retries=3, delay=1.0)
        def call_api():
            ...
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
                    logger.warning(
                        f"[Retry {attempt}/{retries}] {func.__name__} failed: "
                        f"{type(exc).__name__}: {exc}. "
                        f"{'Retrying in {:.1f}s...'.format(wait) if attempt < retries else 'No more retries.'}"
                    )
                    if attempt < retries:
                        time.sleep(wait)
                        wait *= backoff
            raise last_exc  # Re-raise after exhausting retries
        return wrapper
    return decorator


def handle_agent_error(agent_name: str, exc: Exception, fallback_state: dict) -> dict:
    """
    Standardized error handler for LangGraph agent nodes.
    Logs the error and returns a fallback partial state so the pipeline
    can continue rather than crash.

    Args:
        agent_name: Name of the agent (for logging).
        exc: The caught exception.
        fallback_state: Dict of state keys/values to return on error.

    Returns:
        The fallback_state dict.
    """
    logger.error(
        f"[{agent_name}] Unexpected error: {type(exc).__name__}: {exc}",
        exc_info=True,
    )
    return fallback_state
