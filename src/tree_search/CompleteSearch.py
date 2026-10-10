import datetime
import logging


class CompleteSearch:
    def __init__(self):
        pass

    def start_search(self, game, player):
        move_to_position_dict = {}
        possible_moves = player.get_legal_moves(game)

        for i, move in enumerate(possible_moves):
            game.make_move(move)

            if len(game.history) < 10:
                logging.debug("Timestamp : %s", datetime.datetime.now())
                logging.info("Depth : %d", len(game.history))
                logging.debug(f"Move %d/%d", i + 1, len(possible_moves))

            # Unless it's a draw, We keep the game going if we don't know the evaluation of this position
            if game.draw:
                new_eval = True, 0
                move_to_position_dict[move] = new_eval
            else:
                fen = game.get_footprint()
                if fen not in game.position_storage.get_database():
                    game.play()

                new_eval = game.position_storage.get_database().get(fen)
                move_to_position_dict[move] = new_eval

            # We go back to the original position
            game.cancel_move()

        player.evaluate_and_save(game, move_to_position_dict)
