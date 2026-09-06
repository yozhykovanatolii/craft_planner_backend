from fastapi import APIRouter, status
from schemas.user import UserRegisterSchema

auth_router = APIRouter(prefix='/auth')

@auth_router.post('/register', status_code = status.HTTP_201_CREATED)
async def register_user(user_register: UserRegisterSchema):
    return {'input_data': user_register}