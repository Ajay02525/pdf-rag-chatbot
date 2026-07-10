import time

from fastapi import Request

from services.observability.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
)


async def metrics_middleware(request: Request, call_next):

    start = time.perf_counter()

    response = await call_next(request)

    elapsed = time.perf_counter() - start

    endpoint = request.url.path
    method = request.method
    status = str(response.status_code)

    REQUEST_COUNT.labels(
        endpoint=endpoint,
        method=method,
        status=status,
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=endpoint,
        method=method,
    ).observe(elapsed)

    return response
