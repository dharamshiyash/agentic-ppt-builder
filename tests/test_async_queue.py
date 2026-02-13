
import pytest
from unittest.mock import MagicMock, patch
from tools.async_queue import enqueue_job, MockJob

def test_enqueue_job_no_redis():
    """Test fallback to sync execution when Redis is unavailable."""
    # Mock 'q' as None
    with patch('tools.async_queue.q', None):
        mock_func = MagicMock(return_value="success")
        job, is_async = enqueue_job(mock_func, "arg1")
        
        assert is_async is False
        assert isinstance(job, MockJob)
        assert job.result == "success"
        mock_func.assert_called_with("arg1")

def test_enqueue_job_with_redis():
    """Test enqueuing when Redis is available."""
    mock_q = MagicMock()
    mock_job = MagicMock()
    mock_q.enqueue.return_value = mock_job
    
    with patch('tools.async_queue.q', mock_q):
        mock_func = MagicMock()
        job, is_async = enqueue_job(mock_func, "arg1")
        
        assert is_async is True
        assert job == mock_job
        mock_q.enqueue.assert_called_with(mock_func, "arg1")
