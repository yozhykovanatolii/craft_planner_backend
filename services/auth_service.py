from exceptions.authentication_exception import PasswordNotVerifiedException, UserNotFoundException
from exceptions.email_already_used_exception import EmailAlreadyUsedException
from repositories.user_repository import UserRepository
from schemas.token import TokenSchema
from schemas.user import UserLoginSchema, UserRegisterSchema
from security import create_token, get_password_hash, verify_password

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository
        
    async def register_user(self, user_register: UserRegisterSchema):
        db_user = await self.__user_repository.get_user_by_email(user_register.email)
        if db_user is not None:
            raise EmailAlreadyUsedException()
        user_register.password = get_password_hash(user_register.password)
        await self.__user_repository.create_user(user_register)
        
    async def login_user(self, user_login: UserLoginSchema):
        db_user = await self.__user_repository.get_user_by_email(user_login.email)
        if db_user is None:
            raise UserNotFoundException()
        is_password_verified = verify_password(user_login.password, db_user.password)
        if not is_password_verified:
            raise PasswordNotVerifiedException()
        access_token = create_token(token_data = {'sub': str(db_user.id)}, expires_time_minutes = 30, token_type = 'access')
        refresh_token = create_token(token_data = {'sub': str(db_user.id)}, expires_time_minutes = 43200, token_type = 'refresh')
        return TokenSchema(access_token = access_token, refresh_token = refresh_token)