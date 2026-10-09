import logging

from src.utils import PositionStorage
from src.pieces.Elephant import Elephant
from src.pieces.Gazelle import Gazelle
from src.pieces.Lion import Lion
from src.pieces.Zebra import Zebra
import datetime


class Player:
    def __init__(self, game, white_color):
        self.white_color = white_color
        self.pieces_to_be_placed = {
            Elephant(self, game),
            Elephant(self, game),
            Lion(self, game),
            Lion(self, game),
            Zebra(self, game),
            Zebra(self, game),
            Gazelle(self, game),
            Gazelle(self, game),
        }
        self.pieces_placed = set()

        self.pieces_captured = set()

    def get_legal_moves(self, game):
        list_possible_moves = []
        for piece in self.piece_set():
            for x, y in game.constants.SQUARES_INDICES_NO_CORNER:
                # Rules don't allow piece placement in the corners
                if game.board[x][y] is game.empty_square:
                    list_possible_moves.append(("Place", x, y, piece))

        for piece in self.pieces_placed:
            list_possible_moves.extend(piece.get_legal_moves(game))

        return list_possible_moves

    def piece_set(self):
        """
        :return: a list without duplicate of the pieces_to_be_placed list
        """
        result = []
        for piece in self.pieces_to_be_placed:
            if not any(piece.__class__ == p.__class__ for p in result):
                result.append(piece)
        return result

    def make_move(self, game):
        second_loop_needed = True
        # Pruning strategy
        # First loop : We look for an efficient move :
        #       - A move which wins the game on the spot
        #       - A move which gives a position that we know winning
        # If such a move is found, no need to dive any deeper in the tree search
        possible_moves = self.get_legal_moves(game)

        for i, move in enumerate(possible_moves):
            game.make_move(move)
            game.check_winner()
            new_eval = game.position_storage.get_database().get(game.get_footprint())
            game.cancel_move()
            if new_eval is not None and self.is_winning(*new_eval):
                self.evaluate_and_save(game, {move: new_eval})
                logging.info("Trivial pruning found at move %d/%d !", i+1, len(possible_moves))
                second_loop_needed = False
                break

        if second_loop_needed:
            # Second loop : None of the move gives a trivial win
            # We continue the tree search
            move_to_position_dict = {}
            for i, move in enumerate(possible_moves):
                game.make_move(move)

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

                if self.is_winning(*new_eval):
                    # Pruning : if at least one of the moves gives a winning position,
                    # We do not look for the other moves
                    logging.info("Pruning found at move %d/%d !", i, len(possible_moves))
                    break

            self.evaluate_and_save(game, move_to_position_dict)


    def evaluate_and_save(self, game, move_to_position_dict):
        '''
        Computes the best possible move along all the possibilities.
        The best move is used to compute the current position evaluation
        Once the best move is computed, the position evaluation is saved in the database

        :param game: The game with the original position
        :param move_to_position_dict: The correspondance move -> FEN position
        '''
        best_eval = None
        for move, (finished, evaluation) in move_to_position_dict.items():

            if self.is_better(finished, evaluation, best_eval):
                best_move = move
                best_eval = finished, evaluation

        game.position_storage.save_state(game.get_footprint(), False, self.next_eval(*best_eval))


    def update_pieces(self):
        newly_captured = [piece for piece in self.pieces_placed if piece.is_captured]
        for piece in newly_captured:
            self.pieces_placed.discard(piece)
            self.pieces_captured.add(piece)

    def is_better(self, finished, evaluation, best_eval):
        """
        For white, ordering from worst to best is : [Black, -1, -2, -3, ..., 0, ..., +3, +2, +1, White]

        For black, ordering from worst to be is : [White, +1, +2, +3, ..., 0, ..., -3, -2, -1, Black]

        :return: true is evaluation is better than best_eval for the current_player
        """
        if best_eval is None : return True
        if self.white_color:
            if finished != 0:
                return finished == 1
            return evaluation > best_eval[0]
        else:
            if finished != 0:
                return finished == -1
            return evaluation < best_eval[0]

    def next_eval(self, finished, evaluation):
        # Game is finished, M1 for either white or black
        if finished != 0:
            return finished

        if self.white_color:
            if evaluation > 0:
                return evaluation + 1
            else:
                return evaluation
        else:
            if evaluation < 0:
                return evaluation - 1
            else:
                return evaluation

    def get_color(self):
        return self.white_color

    def get_free_piece(self, piece):
        for p in self.pieces_to_be_placed | self.pieces_placed | self.pieces_captured:
            if p.__class__ == piece.__class__:
                return p

    def get_captured_pieces(self):
        return self.pieces_captured

    def get_to_be_placed_pieces(self):
        return self.pieces_to_be_placed

    def is_winning(self, finished, evaluation):
        if self.white_color:
            return finished > 0 or evaluation > 0
        else:
            return finished < 0 or evaluation < 0


