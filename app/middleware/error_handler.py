from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.utils.response import error_response
import logging

logger= logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=error_response("Internal server error", str(exc), 500)
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.detail, None, exc.status_code)
    )