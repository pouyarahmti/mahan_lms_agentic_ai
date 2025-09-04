from functools import wraps
import requests
import logging
from src.lms_agents.base_agent import AgentResponse
import time


logger = logging.getLogger(__name__)


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying failed API calls."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2**attempt))  # Exponential backoff
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")

            logger.error(
                f"All {max_retries} attempts failed. Last error: {last_exception}"
            )
            return AgentResponse(
                success=False,
                error=f"API call failed after {max_retries} attempts: {str(last_exception)}",
            )

        return wrapper

    return decorator
