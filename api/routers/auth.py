from fastapi import APIRouter, Depends, status
from database import get_db
from repositories.user_repository import UserRepository
from schemas.user import UserRegisterSchema
from services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter(prefix='/auth')

@auth_router.post('/register', status_code = status.HTTP_201_CREATED)
async def register_user(user_register: UserRegisterSchema, db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    await auth_service.register_user(user_register)
    return {'input_data': user_register}