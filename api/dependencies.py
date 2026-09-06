from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth_service import AuthService
from services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_user_repository(db: DatabaseSession):
    return UserRepository(db)

def get_auth_service(user_repository: UserRepositoryDependency):
    return AuthService(user_repository)

def get_user_service(user_Repository: UserRepositoryDependency):
    return UserService(user_Repository)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_Service: Annotated[UserService, Depends(get_user_service)]):
    return await user_Service.get_user(token)

DatabaseSession = Annotated[AsyncSession, Depends(get_db)]
UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]