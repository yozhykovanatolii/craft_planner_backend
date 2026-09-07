from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile, status
from api.dependencies import get_current_user, get_user_service
from schemas.user import UserInfoSchema, UserUpdateSchema
from services.user_service import UserService


user_router = APIRouter(prefix='/users')
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
CurrentUser = Annotated[UserInfoSchema, Depends(get_current_user)]

@user_router.get('/me', status_code = status.HTTP_200_OK)
async def get_user(current_user: CurrentUser):
    return current_user

@user_router.patch('/me', status_code = status.HTTP_204_NO_CONTENT)
async def update_user(user_data: UserUpdateSchema, user_service: UserServiceDependency, current_user: CurrentUser):
    await user_service.update_user(current_user.id, user_data)
    
@user_router.post('/me/avatar', status_code = status.HTTP_201_CREATED)
async def upload_user_avatar(user_service: UserServiceDependency, current_user: CurrentUser, file: UploadFile = File(...)):
    file_bytes = await file.read()
    user_avatar_url = user_service.update_user_avatar(current_user.id, file_bytes, file.content_type, file.filename)
    return {'avatar_url': user_avatar_url}
    