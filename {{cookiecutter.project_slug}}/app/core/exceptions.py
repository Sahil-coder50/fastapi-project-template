from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import traceback

from .response import ApiResponse

async def global_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=exc.status_code if getattr(exc, "status_code", None) else 500,
        content=ApiResponse.error_response(
            message=exc.message if getattr(exc, "message", None) else "Internal Server Error",
            error=exc.error if getattr(exc, "error", None) else "Internal Server Error",
        ).model_dump(exclude_none=True),
    )

async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
):
    return JSONResponse(
        status_code=500,
        content=ApiResponse.error_response(
            message=str(exc.orig) if getattr(exc, "orig", None) else "Database Error",
            error=exc.__class__.__name__,
        ).model_dump(exclude_none=True),
    )

class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        error=None,
    ):
        self.status_code = status_code
        self.message = message
        self.error = error