from pwdlib import PasswordHash


def get_password_hash(password: str):
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)

def verify_password(password: str, hash_key: str):
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, hash_key)