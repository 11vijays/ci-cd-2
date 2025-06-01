from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from fastapi import Depends
from app.core import get_db
from app.utils import db_safe


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @db_safe()
    async def create_user(self, user: UserCreate) -> User:
        user = User(**user.model_dump())
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return UserOut.model_validate(user).model_dump()

    @db_safe()
    async def get_all_users(self) -> list[User]:
        result = await self.db.execute(select(User))
        users = result.scalars().all()
        user_data = [UserOut.model_validate(user).model_dump() for user in users]
        return user_data


async def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserService:
    return UserService(db)
