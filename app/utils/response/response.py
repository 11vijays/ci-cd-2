from fastapi.responses import JSONResponse
from typing import Any


def success_response(data: Any, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "code": status_code,
            "data": data,
        },
    )


def error_response(message: str, status_code: int = 400, error: str = ""):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
            "code": status_code,
            **({"error": error} if error else {}),
        },
    )
