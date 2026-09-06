from pydantic import BaseModel, ConfigDict, EmailStr, Field
from schemas.validators import FullNameStr, PasswordStr

class UserRegisterSchema(BaseModel):
    full_name: FullNameStr
    email: EmailStr
    password: PasswordStr
    phone_number: str = Field(pattern=r'^\+380\d{9}$')
    
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: PasswordStr
    
class UserInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    full_name: FullNameStr
    email: EmailStr
    phone_number: str
    avatar_url: str
    
class UserUpdateSchema(BaseModel):
    full_name: FullNameStr
    phone_number: str = Field(pattern=r'^\+380\d{9}$')
    avatar_url: str = Field(min_length=1)