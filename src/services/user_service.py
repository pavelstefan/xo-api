from src.db_client import get_prisma_client
from typing import Union
from prisma.models import User
from prisma.types import UserWhereInput


class UserService:
    @staticmethod
    async def get_user(email: str) -> Union[User, None]:
        prisma = await get_prisma_client()
        return await prisma.user.find_first(
            where=UserWhereInput(
                email=email
            )
        )
