from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy import text
from app.core import engine
from app.routes import v1_router
from app.utils import error_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.execute(text("select 1"))
            print("DB connected")
    except Exception as e:
        print("failed to connect")
        raise e
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return error_response(
        status_code=500,
        message="Something went wrong",
        error=str(exc),
    )


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handle(req: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return error_response(
            message="Api endpoint not found", status_code=exc.status_code or 404
        )

    return error_response(message=exc.detail, status_code=exc.status_code or 404)


@app.get("/health")
def health_check():
    return {"status": "Health is ok"}


app.include_router(v1_router, prefix="/api/v1")
