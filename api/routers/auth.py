from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import get_auth_service
from schemas.user import UserLoginSchema, UserRegisterSchema
from services.auth_service import AuthService

auth_router = APIRouter(prefix='/auth')
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]

@auth_router.post('/register', status_code = status.HTTP_201_CREATED)
async def register_user(user_register: UserRegisterSchema, auth_service: AuthServiceDependency):
    await auth_service.register_user(user_register)
    return {'message': 'Success registration'}

@auth_router.post('/login', status_code = status.HTTP_200_OK)
async def login_user(user_login: UserLoginSchema, auth_service: AuthServiceDependency):
    return await auth_service.login_user(user_login)