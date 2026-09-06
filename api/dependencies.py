from typing import Annotated
from fastapi import Depends
from database import get_db
from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth_service import AuthService


def get_user_repository(db: DatabaseSession):
    return UserRepository(db)

def get_auth_service(user_repository: UserRepositoryDependency):
    return AuthService(user_repository)

DatabaseSession = Annotated[AsyncSession, Depends(get_db)]
UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]