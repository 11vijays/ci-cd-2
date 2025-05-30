from fastapi.responses import JSONResponse
from typing import Any

ACTIONS = {
    "POST": "created",
    "PUT": "updated",
    "PATCH": "modified",
    "DELETE": "deleted",
    "GET": "retrieved",
    "UPLOAD": "uploaded",
    "DEFAULT": "processed",
}

HTTP_METHODS = {
    "CREATE": "POST",
    "UPDATE": "PUT",
    "MODIFY": "PATCH",
    "DELETE": "DELETE",
    "FETCH": "GET",
    "UPLOAD": "UPLOAD",
}


def success_response(
    data: Any, method: str, entity: str, status_code: int = 200
) -> dict:
    action = ACTIONS.get(method, ACTIONS["DEFAULT"])
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "code": status_code,
            "message": f"{entity} {action} successfully",
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
