from fastapi import APIRouter, Depends, HTTPException
from prisma.errors import DataError

from src.models.auth_models import AuthBody, AuthResponse
from src.services.auth_service import AuthService
from src.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post('/login')
async def handle_login(body: AuthBody, user_service: UserService = Depends(UserService),
                       auth_service: AuthService = Depends(AuthService)) -> AuthResponse:
    user = await user_service.get_user(body.email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail='Could not validate credentials'
        )
    password_verified = auth_service.verify_password(
        plain_password=body.password,
        hashed_password=user.passwordHash
    )
    if not password_verified:
        raise HTTPException(
            status_code=401,
            detail='Could not validate credentials'
        )
    token = auth_service.create_access_token({
        'sub': user.email
    })
    return AuthResponse(
        accessToken=token
    )


@router.post('/register')
async def handle_register(body: AuthBody, auth_service: AuthService = Depends(AuthService)) -> AuthResponse:
    try:
        token = await auth_service.create_user(
            email=body.email,
            password=body.password
        )
        return AuthResponse(
            accessToken=token
        )
    except DataError:
        raise HTTPException(
            status_code=400,
            detail='Email already in use'
        )
