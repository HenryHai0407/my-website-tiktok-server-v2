import inspect
from enum import Enum


class ExceptionType(Enum):
    NOT_FOUND = (404, "NOT_FOUND", "Not found")
    UNAUTHORIZED = (401, "UNAUTHORIZED", "Unauthorized")
    FORBIDDEN = (403, "FORBIDDEN", "Forbidden")
    BAD_REQUEST = (400, "BAD_REQUEST", "Bad request")
    ALREADY_EXISTS = (409, "ALREADY_EXISTS", "Already exists")

    def __init__(self, status_code: int, error_code: str, default_message: str):
        self.status_code = status_code
        self.error_code = error_code
        self.default_message = default_message


class AppException(Exception):
    def __init__(self, ex_type: ExceptionType, message: str = None):
        self.status_code = ex_type.status_code
        self.error_code = ex_type.error_code
        self.message = message or ex_type.default_message

        try:
            frame = inspect.stack()[1]
            self._caller_file = frame.filename.split("/")[-1]
            self._caller_line = frame.lineno
            self._caller_func = frame.function
        except Exception:
            self._caller_file = "unknown"
            self._caller_line = -1
            self._caller_func = "unknown"

    def __str__(self):
        return (f"[{self.error_code}] at {self._caller_file}:{self._caller_line} "
                f"in {self._caller_func} - {self.message}")
