from fastapi import APIRouter, Depends
from app.schemas.user import UserOut, UserCreate
from app.services.user import UserService, get_user_service
from app.utils import success_response, HTTP_METHODS

router = APIRouter()

entity = "user"


@router.post("/create", response_model=UserCreate)
async def create_user(
    user: UserCreate, service: UserService = Depends(get_user_service)
):
    user = await service.create_user(user)
    return success_response(data=user, method=HTTP_METHODS["CREATE"], entity=entity)


@router.get("/all", response_model=list[UserOut])
async def get_all_user(service: UserService = Depends(get_user_service)):
    data = await service.get_all_users()
    return success_response(data=data, method=HTTP_METHODS["FETCH"], entity=entity)
