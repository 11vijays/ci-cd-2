import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Azure App Setting
    AZURE_CLIENT_ID: str = os.getenv("AZURE_CLIENT_ID", "")
    AZURE_CLIENT_SECRET: str = os.getenv("AZURE_CLIENT_SECRET", "")
    AZURE_TENANT_ID: str = os.getenv("AZURE_TENANT_ID", "")

    AUTHORITY: str = f"https://login.microsoftonline.com/consumers"
    SCOPE: list[str] = ["https://graph.microsoft.com/.default"]
    REDIRECT_URI = os.getenv(
        "REDIRECT_URI", "http://localhost:8000/api/v1/auth/callback"
    )


settings = Settings()
