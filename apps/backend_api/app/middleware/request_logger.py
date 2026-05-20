"""
Request logging middleware
"""
import time

from fastapi import Request

from app.core.logging_config import get_logger

logger = get_logger(__name__)


async def request_logger_middleware(request: Request, call_next):
    """Log all incoming requests with timing"""
    start_time = time.time()

    # Log request
    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
        client=request.client.host if request.client else None,
    )

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration = time.time() - start_time

    # Log response
    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=f"{duration:.3f}s",
    )

    return response
