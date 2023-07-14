from fastapi import APIRouter, Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.db import database
from models.user import User
from schemas.user import *
from schemas.token import *
from services.auth import AuthService, update_user_refresh_token

auth_route = APIRouter()
security = HTTPBearer()
auth_handler = AuthService()


@auth_route.post('/signup', tags=["Auth"], status_code=status.HTTP_201_CREATED)
async def signup(
    user: UserSignUp
) -> Tokens:
    if user.email == "" or user.password == "":
        raise HTTPException(400)

    has_user = User.get_or_none(User.email == user.email) != None

    if has_user:
        raise HTTPException(status_code=409, detail='Account already exists')

    user = User.create(
        name=user.name,
        email=user.email,
        password_hash=auth_handler.encode_password(user.password)
    )

    access_token = auth_handler.encode_token(user.email)
    refresh_token = auth_handler.encode_refresh_token(user.email)

    update_user_refresh_token(
        user, auth_handler.get_token_hash(refresh_token)
    )

    return Tokens(access_token=access_token, refresh_token=refresh_token)


@auth_route.post('/signin', tags=["Auth"], status_code=status.HTTP_200_OK)
async def signin(
    user_details: UserSignIn
) -> Tokens:
    user = User.get_or_none(User.email == user_details.email)

    if user is None:
        raise HTTPException(status_code=401, detail='Invalid email')

    if not auth_handler.verify_password(user_details.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid password')

    access_token = auth_handler.encode_token(user.email)
    refresh_token = auth_handler.encode_refresh_token(user.email)

    update_user_refresh_token(
        user.id, auth_handler.get_token_hash(refresh_token)
    )

    return Tokens(access_token=access_token, refresh_token=refresh_token)


@auth_route.post('/refresh', tags=["Auth"], status_code=status.HTTP_200_OK)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Tokens:
    refresh_token = credentials.credentials

    user = User.get_or_none(
        User.email == auth_handler.decode_refresh_token(refresh_token)
    )

    if user == None:
        raise HTTPException(status_code=404, detail="User not found")

    if not auth_handler.verify_Tokens(refresh_token, user.token):
        update_user_refresh_token(user.id, None)
        raise HTTPException(status_code=401, detail='Invalid refresh token')

    new_token = auth_handler.refresh_token(refresh_token)
    refresh_token = auth_handler.encode_refresh_token(user.email)

    update_user_refresh_token(
        user.id, auth_handler.get_token_hash(refresh_token))

    return Tokens(access_token=new_token, refresh_token=refresh_token)


@auth_route.post('/logout', tags=["Auth"], status_code=status.HTTP_200_OK)
async def logout(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials

    if (auth_handler.decode_token(token)):
        user = User.get(User.email == auth_handler.decode_token(token))
        update_user_refresh_token(user.id, None)
    else:
        auth_handler.decode_token(token)
