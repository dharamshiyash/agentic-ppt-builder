# utils/async_runner.py
import logging
from redis import Redis
from rq import Queue
from rq.job import Job
import os

logger = logging.getLogger(__name__)

# Connection to Redis (Optional)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_conn = None
q = None

try:
    redis_conn = Redis.from_url(REDIS_URL, socket_connect_timeout=1)
    redis_conn.ping() # Check connection
    q = Queue(connection=redis_conn)
    logger.info("Connected to Redis for async execution.")
except Exception as e:
    logger.warning(f"Redis not available ({e}). Falling back to synchronous execution.")
    redis_conn = None
    q = None

def enqueue_job(func, *args, **kwargs):
    """
    Enqueues a job if Redis is available, otherwise runs instantly (sync fallback).
    Returns:
        job (Job object or MockJob)
        is_async (bool)
    """
    if q:
        job = q.enqueue(func, *args, **kwargs)
        return job, True
    else:
        logger.info("Running job synchronously (No Redis).")
        result = func(*args, **kwargs)
        return MockJob(result), False

class MockJob:
    """Mock Job object for synchronous fallback."""
    def __init__(self, result):
        self._result = result
        self.id = "sync_job"
        self.is_finished = True
        self.is_failed = False
    
    @property
    def result(self):
        return self._result
        
    def refresh(self):
        pass
