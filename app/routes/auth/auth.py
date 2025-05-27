from fastapi import APIRouter, Depends, Request
from app.schema.auth import TokenResponse, LoginRequest
from app.services.auth import AuthService, get_auth_service

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.login_user(data)


@router.get("/callback")
async def get_azure_token(
    request: Request, auth_service: AuthService = Depends(get_auth_service)
):
    code = request.query_params.get("code")
    return auth_service.azure_token(code)
