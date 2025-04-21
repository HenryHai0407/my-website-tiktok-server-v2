from config.logging_config import logger
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .custom_exception import AppException


async def app_exception_handler(request: Request, err: AppException):
    logger.error(f"AppException {err}")
    return JSONResponse(
        status_code=err.status_code,
        content={
            "error_code": err.error_code,
            "message": err.message
        }
    )


async def http_exception_handler(request: Request, err: StarletteHTTPException):
    logger.error(f"HTTPException: {err}")
    return JSONResponse(
        status_code=err.status_code,
        content={"error_code": "HTTP_ERROR", "message": err.detail}
    )


async def validation_exception_handler(request: Request, err: RequestValidationError):
    logger.error(f"ValidationError: {err}")
    return JSONResponse(
        status_code=422,
        content={
            "error_code": "VALIDATION_ERROR",
            "message": err.errors()
        }
    )


def register_exceptions(app: FastAPI):
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError,
                              validation_exception_handler)
