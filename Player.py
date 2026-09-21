import copy
import random

import PositionStorage
import Strategeti
from Pieces.Elephant import Elephant
from Pieces.Gazelle import Gazelle
from Pieces.Lion import Lion
from Pieces.Piece import Piece
from Pieces.Zebra import Zebra


class Player:
    def __init__(self, white_color, database : PositionStorage.PositionStorage):
        self.white_color = white_color
        self.position_storage : PositionStorage.PositionStorage = database
        self.pieces_to_be_placed = {
            Elephant(self),
            Elephant(self),
            Lion(self),
            Lion(self),
            Zebra(self),
            Zebra(self),
            Gazelle(self),
            Gazelle(self),
        }
        self.pieces_placed = set()

        self.pieces_captured = set()

    def get_legal_moves(self, board):
        list_possible_moves = []
        for piece in self.piece_set():
            for x in range(4):
                for y in range(4):
                    if (x not in [0, 3] or y not in [0, 3]) and board[x][y] == '':
                        list_possible_moves.append(("Place", x, y, piece))

        for piece in self.pieces_placed:
            list_possible_moves.extend(piece.get_legal_moves(board))

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
        move_to_position_dict = {}
        possible_moves = self.get_legal_moves(game.get_board())

        for move in possible_moves:
            game.FEN_safety()
            game.make_move(move)
            game.FEN_safety()

            print("Depth : " + str(len(game.history)))

            fen = game.get_FEN_board()
            # We keep the game going if we don't know the evaluation of this position
            if fen not in self.position_storage.get_database():
                game.play()
            else:
                print("Known position : " + fen)
            move_to_position_dict[move] = self.position_storage.get_database()[fen]
            print(move, fen)

            # We go back to the original position
            game.FEN_safety()
            game.cancel_move()
            game.FEN_safety()


        print("New position solved")
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

            if self.is_better(evaluation, best_eval):
                best_move = move
                best_eval = evaluation

        self.position_storage.save_state(game.get_FEN_board(), False, self.next_eval(best_eval))


    def update_pieces(self):
        newly_captured = [piece for piece in self.pieces_placed if piece.is_captured]
        for piece in newly_captured:
            self.pieces_placed.discard(piece)
            self.pieces_captured.add(piece)

    def assert_copy_safety(self, game, tmp_game):
        for i in range(len(game.player1.pieces_placed)):
            assert id(game.player1.pieces_placed[i]) != id(tmp_game.player1.pieces_placed[i])

    def is_better(self, evaluation, best_eval):
        """
        For white, ordering from worst to best is : [Black, -1, -2, -3, ..., 0, ..., +3, +2, +1, White]

        For black, ordering from worst to be is : [White, +1, +2, +3, ..., 0, ..., -3, -2, -1, Black]

        :return: true is evaluation is better than best_eval for the current_player
        """
        if best_eval is None : return True
        if self.white_color:
            if isinstance(evaluation, int) and isinstance(best_eval, int):
                return evaluation > best_eval
            elif isinstance(evaluation, str):
                return evaluation == "White"
            else:
                return best_eval == "Black"
        else:
            if isinstance(evaluation, int) and isinstance(best_eval, int):
                return evaluation < best_eval
            elif isinstance(evaluation, str):
                return evaluation == "Black"
            else:
                return best_eval == "White"

    def next_eval(self, evaluation):
        if self.white_color:
            if evaluation == "Black" or (isinstance(evaluation, int) and evaluation <= 0):
                return evaluation
            elif evaluation == "White":
                return 1
            else:
                return evaluation + 1
        else:
            if evaluation == "White" or (isinstance(evaluation, int) and evaluation >= 0):
                return evaluation
            elif evaluation == "Black":
                return -1
            else:
                return evaluation + 1

    def get_color(self):
        return self.white_color

    def get_free_piece(self, piece):
        for p in self.pieces_to_be_placed | self.pieces_placed | self.pieces_captured:
            if p.__class__ == piece.__class__:
                return p


