from services.auth import AuthService
from fastapi.security import HTTPAuthorizationCredentials
from functools import wraps

auth_handler = AuthService()


def private(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if auth_handler.decode_token(kwargs["credentials"].credentials):
            return await func(*args, **kwargs)
        else:
            auth_handler.decode_token(kwargs["credentials"].credentials)

    return wrapper
