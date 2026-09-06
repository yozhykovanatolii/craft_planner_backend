import jwt
from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash
from config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = 'HS256'


def get_password_hash(password: str):
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)

def verify_password(password: str, hash_key: str):
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, hash_key)

def create_token(token_data: dict, expires_time_minutes, token_type: str):
    payload = token_data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_time_minutes)
    payload.update({'exp': expire, 'type': token_type})
    encode_jwt = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    return encode_jwt