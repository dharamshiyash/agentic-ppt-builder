"""
Async Queue Tool
----------------
Optional async job execution using Redis and RQ (Redis Queue).
Falls back to synchronous execution if Redis is not available.
"""

import logging
import os

logger = logging.getLogger(__name__)

# Connection to Redis (Optional)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_conn = None
q = None

try:
    from redis import Redis
    from rq import Queue
    redis_conn = Redis.from_url(REDIS_URL, socket_connect_timeout=1)
    redis_conn.ping()
    q = Queue(connection=redis_conn)
    logger.info("Connected to Redis for async execution.")
except Exception as e:
    logger.warning(f"Redis not available ({e}). Falling back to synchronous execution.")
    redis_conn = None
    q = None


def enqueue_job(func, *args, **kwargs):
    """
    Enqueue a job for async execution if Redis is available.

    Falls back to synchronous (immediate) execution if Redis is
    not connected.

    Args:
        func: The callable to execute.
        *args: Positional arguments for the callable.
        **kwargs: Keyword arguments for the callable.

    Returns:
        tuple: (job_or_mock, is_async) where:
            - ``job_or_mock``: An RQ Job object or MockJob for sync execution
            - ``is_async``: True if the job was queued asynchronously
    """
    if q:
        job = q.enqueue(func, *args, **kwargs)
        return job, True
    else:
        logger.info("Running job synchronously (No Redis).")
        result = func(*args, **kwargs)
        return MockJob(result), False


class MockJob:
    """
    Mock Job object for synchronous fallback.

    Mimics the RQ Job interface so callers don't need to
    differentiate between async and sync execution.
    """

    def __init__(self, result):
        self._result = result
        self.id = "sync_job"
        self.is_finished = True
        self.is_failed = False

    @property
    def result(self):
        """Return the job result."""
        return self._result

    def refresh(self):
        """No-op for sync jobs."""
        pass
