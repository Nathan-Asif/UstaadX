"""
Global error handling middleware
"""
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logging_config import get_logger

logger = get_logger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """Catch and log all unhandled exceptions"""
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(
            "unhandled_exception",
            method=request.method,
            path=request.url.path,
            error=str(exc),
            exc_info=True,
        )

        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "type": "internal_error",
            },
        )
