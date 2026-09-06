from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import get_auth_service
from schemas.user import UserRegisterSchema
from services.auth_service import AuthService

auth_router = APIRouter(prefix='/auth')
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]

@auth_router.post('/register', status_code = status.HTTP_201_CREATED)
async def register_user(user_register: UserRegisterSchema, auth_service: AuthServiceDependency):
    await auth_service.register_user(user_register)
    return {'input_data': user_register}