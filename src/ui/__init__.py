from typing import Optional

from ..types import Player
from ..service import place_stone, check_draw
from ..config import create_initial_game_state, BOARD_SIZE


def display_board(board):
    print("\n   " + " ".join(f"{i:2d}" for i in range(BOARD_SIZE)))
    for i, row in enumerate(board):
        row_str = f"{i:2d} "
        for cell in row:
            if cell == Player.BLACK:
                row_str += " X "
            elif cell == Player.WHITE:
                row_str += " O "
            else:
                row_str += " . "
        print(row_str)
    print()


def get_move_input() -> Optional[dict]:
    while True:
        user_input = input("Enter move (row,col) or 'quit': ").strip()
        if user_input.lower() in ("quit", "q"):
            return None
        try:
            parts = user_input.split(",")
            if len(parts) != 2:
                raise ValueError
            row = int(parts[0].strip())
            col = int(parts[1].strip())
            if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
                raise ValueError
            return {"row": row, "col": col}
        except ValueError:
            print("Invalid input. Enter as row,col (e.g., 7,7) or 'quit' to exit.")


def run_cli():
    state = create_initial_game_state()

    while not state["game_over"]:
        display_board(state["board"])
        current = state["current_player"]
        print(f"Current player: {current.name}")

        move = get_move_input()
        if move is None:
            print("Game aborted.")
            return

        state = place_stone(state, move)

        if state["game_over"]:
            display_board(state["board"])
            winner = state["winner"]
            print(f"Winner: {winner.name}!")
            return

        if check_draw(state):
            display_board(state["board"])
            print("Game ended in a draw!")
            return
