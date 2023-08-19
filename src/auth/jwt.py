from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from prisma.models import User

from src.services.user_service import UserService
from src.settings import settings


async def verify_jwt(token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token or expired token.",
    )
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await UserService.get_user(username)
    if user is None:
        raise credentials_exception
    return user


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            return await verify_jwt(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
