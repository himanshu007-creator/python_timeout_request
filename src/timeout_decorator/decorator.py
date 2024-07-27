import asyncio
import functools
import logging
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError

import colorlog

# Set up colored logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s:%(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': '#f4afc2',
        'ERROR': '#f4afc2',
        'CRITICAL': 'red,bg_white',
    }
))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class TimeoutError(Exception):
    """Custom error for timeout"""
    pass

def timeout_decorator(timeout, callback=None, custom_error=None):
    """
    Decorator to add a timeout to a function (sync or async).
    
    :param timeout: Timeout in seconds
    :param callback: Optional callback function to be called on timeout
    :param custom_error: Optional custom error to be raised on timeout
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                return asyncio.create_task(async_wrapper(*args, **kwargs))
            else:
                return sync_wrapper(*args, **kwargs)

        async def async_wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            except asyncio.TimeoutError:
                logger.warning(f"Async function {func.__name__} timed out.")
                if callback:
                    callback(func.__name__, *args, **kwargs)
                if custom_error:
                    raise custom_error(f"Async function {func.__name__} timed out.")
                return None
            except Exception as e:
                logger.error(f"Async function {func.__name__} raised an exception: {e}")
                raise

        def sync_wrapper(*args, **kwargs):
            result = [None]
            exception = [None]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(target)
                try:
                    future.result(timeout=timeout)
                except FuturesTimeoutError:
                    logger.warning(f"Sync function {func.__name__} timed out.")
                    if callback:
                        callback(func.__name__, *args, **kwargs)
                    if custom_error:
                        raise custom_error(f"Sync function {func.__name__} timed out.")
                    return None

            if exception[0]:
                logger.error(f"Sync function {func.__name__} raised an exception: {exception[0]}")
                raise exception[0]
            return result[0]

        return wrapper

    return decorator