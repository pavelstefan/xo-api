from prisma.enums import GameCell
from pydantic import BaseModel


class GameMove(BaseModel):
    cell: GameCell


win_config = [
    [GameCell.A1, GameCell.A2, GameCell.A3],
    [GameCell.B1, GameCell.B2, GameCell.B3],
    [GameCell.C1, GameCell.C2, GameCell.C3],
    [GameCell.A1, GameCell.B2, GameCell.C3],
    [GameCell.C1, GameCell.B2, GameCell.A3],
]
