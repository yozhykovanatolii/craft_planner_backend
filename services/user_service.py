from exceptions.authentication_exception import TokenTypeException, UserNotFoundException
from repositories.user_repository import UserRepository
from schemas.user import UserInfoSchema, UserUpdateSchema
from security import decode_access_token

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository
            
    async def get_user(self, token: str):
        payload = decode_access_token(token)
        token_type = payload.get('type')
        if token_type != 'access':
            raise TokenTypeException()
        user_id = int(payload.get('sub'))
        db_user = await self.__user_repository.get_user_by_id(user_id)
        if db_user is None:
            raise UserNotFoundException()
        return UserInfoSchema.model_validate(db_user)
    
    async def update_user(self, user_id: int, user_data: UserUpdateSchema):
        update_data = user_data.model_dump(exclude_unset=True)
        update_data["id"] = user_id
        await self.__user_repository.update_user(update_data)