from typing import Union

from fastapi import HTTPException
from prisma.enums import GameStatus, GameCell
from prisma.models import Game, User, Move
from prisma.types import (
    GameCreateInput, UsersOnGamesCreateManyNestedWithoutRelationsInput, UsersOnGamesCreateWithoutRelationsInput,
    GameWhereInput, UsersOnGamesCreateInput, GameInclude, FindManyUsersOnGamesArgsFromGame, GameUpdateInput,
    MoveCreateInput, GameWhereUniqueInput
)

from src.db_client import get_prisma_client
from src.models.game_models import win_config


class GameService:
    @staticmethod
    async def create_game(user: User) -> Game:
        prisma = await get_prisma_client()
        game = await prisma.game.create(
            data=GameCreateInput(
                status=GameStatus.open,
                playerToMove=user.id,
                users=UsersOnGamesCreateManyNestedWithoutRelationsInput(
                    create=[
                        UsersOnGamesCreateWithoutRelationsInput(
                            userId=user.id
                        )
                    ]
                )
            ),
        )
        return game

    @staticmethod
    async def get_game(game_id: int) -> Union[Game, None]:
        prisma = await get_prisma_client()
        game = await prisma.game.find_first(
            where=GameWhereInput(
                id=game_id
            ),
            include=GameInclude(
                users=FindManyUsersOnGamesArgsFromGame(
                    include={
                        'user': True
                    }
                ),
                moves=True,
            )
        )
        return game

    @staticmethod
    async def join_game(user: User, game_id: int) -> Game:
        game = await GameService.get_game(game_id)
        if not game:
            raise HTTPException(
                status_code=400,
                detail='Invalid game'
            )
        if game.status != GameStatus.open:
            raise HTTPException(
                status_code=400,
                detail='Game is not open'
            )
        if game.users[0].user.id == user.id:
            raise HTTPException(
                status_code=400,
                detail='Already joined'
            )

        prisma = await get_prisma_client()
        await prisma.usersongames.create(
            data=UsersOnGamesCreateInput(
                userId=user.id,
                gameId=game.id,
            )
        )

        game = await prisma.game.update(
            where=GameWhereUniqueInput(
                id=game_id
            ),
            data=GameUpdateInput(
                status=GameStatus.active
            ),
            include=GameInclude(
                users=FindManyUsersOnGamesArgsFromGame(
                    include={
                        'user': True
                    }
                ),
                moves=True,
            )
        )

        return game

    @staticmethod
    async def list_games() -> list[Game]:
        prisma = await get_prisma_client()
        games = await prisma.game.find_many(
            include=GameInclude(
                users=FindManyUsersOnGamesArgsFromGame(
                    include={
                        'user': True
                    }
                )
            )
        )
        return games

    @staticmethod
    async def add_move(user: User, game_id: int, cell: GameCell) -> Game:
        game = await GameService.get_game(game_id)

        # check if move is valid
        detail = None
        if game.status != GameStatus.active:
            detail = 'Game is not active'
        elif game.playerToMove != user.id:
            detail = 'Not your turn or you are not part of the game'

        for move in game.moves:
            if move.cell == cell:
                detail = 'Invalid move'

        if detail:
            raise HTTPException(
                status_code=400,
                detail=detail
            )

        # add move to the game
        prisma = await get_prisma_client()
        p1 = game.users[0].user
        p2 = game.users[1].user

        player_to_move = p1 if p1.id != game.playerToMove else p2
        await prisma.move.create(
            data=MoveCreateInput(
                gameId=game.id,
                userId=user.id,
                cell=cell,
            )
        )

        # check if game is finished
        def select_moves(m: Move) -> bool:
            return m.userId == user.id

        def map_moves(m: Move) -> GameCell:
            return m.cell

        player_moves: list[GameCell] = [*map(map_moves, filter(select_moves, game.moves)), cell]
        did_win = False

        for config in win_config:
            win = True
            for c in config:
                if c not in player_moves:
                    win = False
                    break
            if win:
                did_win = True
                break

        status = GameStatus.active
        if did_win:
            status = GameStatus.ended_win
        elif len(game.moves) == 8:
            status = GameStatus.ended_draw

        # update the game
        game = await prisma.game.update(
            where=GameWhereUniqueInput(
                id=game.id
            ),
            data=GameUpdateInput(
                playerToMove=player_to_move.id,
                status=status,
                winnerId=user.id if did_win else None
            ),
            include=GameInclude(
                users=FindManyUsersOnGamesArgsFromGame(
                    include={
                        'user': True
                    }
                ),
                moves=True,
            )
        )

        return game
