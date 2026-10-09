import logging
import os

from src.utils.PositionStorage import PositionStorage
from src.utils.Strategeti import Strategeti

storage = PositionStorage()

if os.path.exists("../tests/database.pkl"):
    logging.error("Loading database...")
    storage.load_database()
    init_size = len(storage.positions)
    logging.error(f"Database of {init_size} elements successfully loaded")
else:
    logging.error("Cannot find database at ../tests/database.pkl. Restarting the solving from scratch.")


game = Strategeti(3, storage)

while True:
    available_moves = game.player1.get_legal_moves(game) if game.white_to_move else game.player2.get_legal_moves(game)
    print(f"{'White' if game.white_to_move else 'Black'} to move : ")
    for i, move in enumerate(available_moves):
        game.make_move(move)
        evaluation = storage.get_database().get(game.get_footprint())
        game.cancel_move()

        print(f"[{i}] : {move}, evaluation = {evaluation}")
    print()

    player_choice = ""
    while not player_choice.isdigit() or int(player_choice) >= len(available_moves):
        player_choice = input()
    player_choice = int(player_choice)
    game.make_move(available_moves[player_choice])
    game.show_board()
    if game.check_winner():
        print("Game is finished")
        break

