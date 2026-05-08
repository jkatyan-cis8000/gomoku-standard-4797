from typing import List, Tuple

from ..config import BOARD_SIZE, get_cell, set_cell
from ..types import Board, Cell, GameState, Player, Position

__all__ = ["check_win", "get_valid_moves", "place_stone", "check_draw"]


def check_win(board: Board, position: Position, player: Player) -> bool:
    row = position["row"]
    col = position["col"]
    
    directions = [
        [(0, 1), (0, -1)],  
        [(1, 0), (-1, 0)],  
        [(1, 1), (-1, -1)], 
        [(1, -1), (-1, 1)], 
    ]
    
    for direction_pairs in directions:
        count = 1
        for dx, dy in direction_pairs:
            r, c = row + dx, col + dy
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if get_cell(board, {"row": r, "col": c}) == player:
                    count += 1
                    r += dx
                    c += dy
                else:
                    break
        if count >= 5:
            return True
    return False


def get_valid_moves(game_state: GameState) -> List[Position]:
    board = game_state["board"]
    moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] is None:
                moves.append({"row": row, "col": col})
    return moves


def place_stone(game_state: GameState, position: Position) -> GameState:
    if game_state["game_over"]:
        return game_state
    
    if not (0 <= position["row"] < BOARD_SIZE and 0 <= position["col"] < BOARD_SIZE):
        return game_state
    
    board = game_state["board"]
    if board[position["row"]][position["col"]] is not None:
        return game_state
    
    new_board = [row[:] for row in board]
    player = game_state["current_player"]
    set_cell(new_board, position, player)
    
    new_game_state = {
        "board": new_board,
        "current_player": Player.WHITE if player == Player.BLACK else Player.BLACK,
        "game_over": False,
        "winner": None,
    }
    
    if check_win(new_board, position, player):
        new_game_state["game_over"] = True
        new_game_state["winner"] = player
    
    return new_game_state


def check_draw(game_state: GameState) -> bool:
    board = game_state["board"]
    for row in board:
        if None in row:
            return False
    return True
