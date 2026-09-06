from pydantic import BaseModel, EmailStr, Field
from schemas.validators import FullNameStr, PasswordStr

class UserRegisterSchema(BaseModel):
    full_name: FullNameStr
    email: EmailStr
    password: PasswordStr
    phone_number: str = Field(pattern=r'^\+380\d{9}$')