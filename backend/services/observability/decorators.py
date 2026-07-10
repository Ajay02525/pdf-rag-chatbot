import time
from functools import wraps

from services.observability.metrics import RAG_STEP_LATENCY


def measure_latency(step_name: str):
    """
    Decorator to measure execution time of a function
    and publish it to Prometheus.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start = time.perf_counter()

            try:
                return func(*args, **kwargs)

            finally:
                elapsed = time.perf_counter() - start

                RAG_STEP_LATENCY.labels(step=step_name).observe(elapsed)

        return wrapper

    return decorator


def measure_async_latency(step_name: str):

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            start = time.perf_counter()

            try:
                return await func(*args, **kwargs)

            finally:
                elapsed = time.perf_counter() - start

                RAG_STEP_LATENCY.labels(step=step_name).observe(elapsed)

        return wrapper

    return decorator
