from fastapi import APIRouter
from .user import user_router
from .auth import auth_router

v1_router = APIRouter()

v1_router.include_router(user_router, prefix="/user", tags=["Users"])
v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
