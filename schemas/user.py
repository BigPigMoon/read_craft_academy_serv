from pydantic import BaseModel


class UserSignUp(BaseModel):
    email: str
    password: str
    name: str


class UserSignIn(BaseModel):
    email: str
    password: str
