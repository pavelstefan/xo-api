from fastapi import APIRouter, Depends
from prisma.models import User, Game

from src.auth.jwt import JWTBearer
from src.models.game_models import GameMove
from src.services.game_service import GameService

router = APIRouter(
    prefix="/game",
    tags=["game"],
    responses={404: {"description": "Not found"}},
)


@router.post('')
async def handle_create_game(user: User = Depends(JWTBearer()), game_service: GameService = Depends()) -> Game:
    return await game_service.create_game(user)


@router.get('')
async def handle_list_games(game_service: GameService = Depends()) -> list[Game]:
    return await game_service.list_games()


@router.post('/{game_id}')
async def handle_join_game(game_id: int, user: User = Depends(JWTBearer()),
                           game_service: GameService = Depends()) -> Game:
    return await game_service.join_game(
        user=user,
        game_id=int(game_id)
    )


@router.get('/{game_id}')
async def handle_get_game(game_id: int, game_service: GameService = Depends()) -> Game:
    return await game_service.get_game(game_id)


@router.post('/move/{game_id}')
async def handle_add_move(body: GameMove, game_id: int, user: User = Depends(JWTBearer()),
                          game_service: GameService = Depends()):
    return await game_service.add_move(
        user=user,
        cell=body.cell,
        game_id=int(game_id)
    )
