from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import pyodbc


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # show SQL in logs if DEBUG=true
    future=True,
)

# Create the sessionmaker factory
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for model declarations
Base = declarative_base()


# Dependency for getting an async DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
