from fastapi import APIRouter, Depends
from prisma.models import User

from src.auth.jwt import JWTBearer

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post('/me')
async def handle_get_user(user: User = Depends(JWTBearer())) -> User:
    return user
