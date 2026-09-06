from exceptions.email_already_used_exception import EmailAlreadyUsedException
from repositories.user_repository import UserRepository
from schemas.user import UserRegisterSchema

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository
        
    async def register_user(self, user_register: UserRegisterSchema):
        db_user = await self.__user_repository.get_user_by_email(user_register.email)
        if db_user is not None:
            raise EmailAlreadyUsedException()