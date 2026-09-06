import re
from typing import Annotated
from pydantic import AfterValidator, Field

def validate_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[#@$!%*?&]).{8,}$'
    if not re.match(pattern, password):
        raise ValueError('Password is too weak')
    return password

def validate_full_name(full_name):
    full_name = full_name.strip()
    pattern = r'[A-Za-zА-Яа-яІіЇїЄєҐґ]+(?: [A-Za-zА-Яа-яІіЇїЄєҐґ]+)*'
    if not full_name:
        raise ValueError('Full name cannot be empty')
    if not re.fullmatch(pattern, full_name):
        raise ValueError('Full name can contain only letters and spaces')
    return full_name

PasswordStr = Annotated[str, AfterValidator(validate_password)]
FullNameStr = Annotated[str, Field(min_length=1, max_length=100), AfterValidator(validate_full_name)]