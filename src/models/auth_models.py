from pydantic import BaseModel


class AuthBody(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    accessToken: str
