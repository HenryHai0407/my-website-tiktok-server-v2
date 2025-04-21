from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from utils.security_util import SecurityUtil
import re


PUBLIC_PATHS = (
    "/", "/docs", "/openapi.json",
    "/api/v1/auth/register", "/api/v1/auth/login",
)

PUBLIC_REGEX = [
    (re.compile(r"^/api/v1/categories/?$"), ["GET"]),
    (re.compile(r"^/api/v1/categories/\d+$"), ["GET"]),
    (re.compile(r"^/api/v1/products/?$"), ["GET"]),
    (re.compile(r"^/api/v1/products/\d+$"), ["GET"]),
    (re.compile(r"^/api/v1/products/search$"),["GET"]),
    (re.compile(r"^/api/v1/products/hot_product"),["GET"]),
]

# These two variables (PUBLIC_PATHS and PUBLIC_REGEX) help you define which routes don’t need authentication.

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ("OPTIONS", "HEAD") or request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        for pattern, methods in PUBLIC_REGEX:
            if pattern.match(request.url.path) and request.method in methods:
                return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "error_code": "UNAUTHORIZED",
                    "error_message": "Unauthorized"
                }
            )

        token = auth_header.split(" ")[1]
        try:
            payload = SecurityUtil.verify_token(token)
            request.state.user = payload
        except Exception:
            return JSONResponse(
                status_code=401,
                content={
                    "error_code": "UNAUTHORIZED",
                    "error_message": "Unauthorized"
                }
            )

        return await call_next(request)
