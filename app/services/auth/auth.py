from app.schemas.auth import LoginRequest, TokenResponse
from msal import ConfidentialClientApplication
from app.core import settings


class AuthService:
    def login_user(user_data: LoginRequest) -> TokenResponse:
        return {}

    def azure_token(code: str) -> TokenResponse:

        app = ConfidentialClientApplication(
            client_id=settings.AZURE_CLIENT_ID,
            client_credential=settings.AZURE_CLIENT_SECRET,
            authority=settings.AUTHORITY,
        )

        result = app.acquire_token_by_authorization_code(
            code=code, scopes=settings.SCOPE, redirect_uri=settings.REDIRECT_URI
        )

        if "access_token" not in result:
            raise Exception(
                result.get(
                    "error_description",
                    "Invalid credentials or authentication failure.",
                )
            )

        return TokenResponse(
            access_token=result["access_token"],
            token_type=result.get("token_type", "Bearer"),
            expires_in=result.get("expires_in"),
        )


async def get_auth_service() -> AuthService:
    return AuthService
