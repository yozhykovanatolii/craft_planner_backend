from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas.user import UserRegisterSchema

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db
        
    async def create_user(self, userRegister: UserRegisterSchema):
        db_user = User(full_name = userRegister.full_name, phone_number = userRegister.phone_number, email = userRegister.email, password = userRegister.password)
        self.__db.add(db_user)
        await self.__db.commit()
        await self.__db.refresh(db_user)
        return db_user
        
    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: int):
        return await self.__db.get(User, user_id)
    
    async def update_user(self, update_data: dict):
        await self.__db.execute(update(User), [update_data])
        await self.__db.commit()