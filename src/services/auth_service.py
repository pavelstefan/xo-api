from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from prisma.types import UserCreateInput

from src.db_client import get_prisma_client
from src.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_LIFETIME_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def create_user(email: str, password: str) -> str:
        prisma = await get_prisma_client()
        user = await prisma.user.create(
            data=UserCreateInput(
                email=email,
                passwordHash=AuthService.get_password_hash(password)
            )
        )

        token = AuthService.create_access_token({
            'sub': user.email
        })

        return token
