import copy
import random
import Strategeti
from Pieces.Elephant import Elephant
from Pieces.Gazelle import Gazelle
from Pieces.Lion import Lion
from Pieces.Piece import Piece
from Pieces.Zebra import Zebra


class Player:
    def __init__(self, white_color, database):
        self.white_color = white_color
        self.database = database
        self.pieces_to_be_placed = [
            Elephant(white_color),
            Elephant(white_color),
            Lion(white_color),
            Lion(white_color),
            Zebra(white_color),
            Zebra(white_color),
            Gazelle(white_color),
            Gazelle(white_color),
        ]
        self.pieces_placed = []

        self.pieces_captured = []

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
        for move in self.get_legal_moves(game.get_board()):
            tmp_game = copy.deepcopy(game)
            tmp_game.set_database(game.get_database())

            print(f"List of moves : {self.get_legal_moves(game.get_board())}")
            print(f"Selected move : {move}")
            tmp_game.make_move_on_board(move)

            # We keep the game going
            tmp_game.play()



    def update_pieces(self):
        newly_captured = [piece for piece in self.pieces_placed if piece.is_captured]
        for piece in newly_captured:
            self.pieces_placed.remove(piece)
            self.pieces_captured.append(piece)
            print(f"Piece captured : {piece}")
