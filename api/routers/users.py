from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import get_current_user, get_user_service
from schemas.user import UserInfoSchema
from services.user_service import UserService


user_router = APIRouter(prefix='/users')
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
CurrentUser = Annotated[UserInfoSchema, Depends(get_current_user)]

@user_router.get('/me', status_code = status.HTTP_200_OK)
async def get_user(current_user: CurrentUser):
    return current_user