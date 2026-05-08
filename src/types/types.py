from enum import Enum
from typing import Dict, List, Optional


class Player(Enum):
    BLACK = "X"
    WHITE = "O"


class GameResult:
    IN_PROGRESS = "in_progress"
    BLACK_WINS = "black_wins"
    WHITE_WINS = "white_wins"
    DRAW = "draw"


class Move:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col


Position = Dict[str, int]

Cell = Optional["Player"]

Board = List[List[Cell]]

GameState = Dict[str, any]
