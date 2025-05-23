from fastapi import APIRouter, Depends
from app.schema.user import UserOut, UserCreate
from app.services.user import UserService, get_user_service
from app.utils import success_response

router = APIRouter()


@router.post("/create", response_model=UserCreate)
async def create_user(
    user: UserCreate, service: UserService = Depends(get_user_service)
):
    user = await service.create_user(user)
    return user


@router.get("/all", response_model=list[UserOut])
async def get_all_user(service: UserService = Depends(get_user_service)):
    data = await service.get_all_users()
    return success_response(data=data)
