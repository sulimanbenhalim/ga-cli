"""Retry logic with exponential backoff for API calls"""

import time
import functools
from google.api_core import exceptions
from ga_cli.logging_config import logger


def retry_on_transient_error(max_retries=3, backoff_factor=2):
    """Decorator for retrying on transient errors

    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Multiplier for exponential backoff delay
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (exceptions.ServiceUnavailable,
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError) as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Max retries ({max_retries}) exceeded for {func.__name__}")
                        raise

                    wait_time = backoff_factor ** retries
                    logger.warning(
                        f"Transient error in {func.__name__}, "
                        f"retrying in {wait_time}s (attempt {retries}/{max_retries}): {str(e)}"
                    )
                    time.sleep(wait_time)

            return func(*args, **kwargs)
        return wrapper
    return decorator
