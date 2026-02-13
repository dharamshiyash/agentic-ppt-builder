import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

logger = logging.getLogger(__name__)

def log_retry_attempt(retry_state):
    """Log retry attempts."""
    logger.warning(f"Retrying {retry_state.fn.__name__} due to error: {retry_state.outcome.exception()} (Attempt {retry_state.attempt_number})")

# Standard retry configuration for API calls
# Retries up to 3 times with exponential backoff starting at 1s up to 10s
api_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.RequestException, Exception)), # Broad exception for now, ideally specific
    before_sleep=log_retry_attempt,
    reraise=True
)
