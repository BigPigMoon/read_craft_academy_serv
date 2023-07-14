from fastapi import APIRouter, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.user import UserOut
from models.user import User
from guard.private import private
from services.auth import AuthService
from fastapi.security import HTTPAuthorizationCredentials


auth_handler = AuthService()
user_route = APIRouter()
security = HTTPBearer()


@user_route.get("/", tags=["User"], response_model=list[UserOut], status_code=status.HTTP_200_OK)
@private
async def get_users(credentials: HTTPAuthorizationCredentials = Security(security)) -> list[UserOut]:
    users = User.select()
    out_users = []
    for user in users:
        out_users.append(UserOut(name=user.name))
    return out_users
