from typing import Dict, List, Optional

from ..types import Board, Cell, GameState, Player, Position

BOARD_SIZE = 15


def create_empty_board() -> Board:
    return [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def create_initial_game_state() -> GameState:
    return {
        "board": create_empty_board(),
        "current_player": Player.BLACK,
        "game_over": False,
        "winner": None,
    }


def get_cell(board: Board, position: Position) -> Cell:
    row = position["row"]
    col = position["col"]
    return board[row][col]


def set_cell(board: Board, position: Position, player: Player) -> None:
    row = position["row"]
    col = position["col"]
    board[row][col] = player


def is_valid_position(position: Position) -> bool:
    row = position["row"]
    col = position["col"]
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
