from fastapi import APIRouter

router = APIRouter(
    prefix="/game",
    tags=["game"],
    responses={404: {"description": "Not found"}},
)


@router.post('/create-game')
async def handle_create_game():
    return
