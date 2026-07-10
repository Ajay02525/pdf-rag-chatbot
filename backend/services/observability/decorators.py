import functools
import time
import asyncio


def measure_latency(_name: str):
    def decorator(func):

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    return await func(*args, **kwargs)
                finally:
                    _ = time.perf_counter() - start

            return async_wrapper

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                _ = time.perf_counter() - start

        return wrapper

    return decorator
