import logging
from functools import wraps
from typing import Callable, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_request(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator for logging request details.  This version supports async functions.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logging.info(f"Request received for: {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            logging.info(f"Request completed for: {func.__name__} with result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            raise
    import asyncio
    return wrapper