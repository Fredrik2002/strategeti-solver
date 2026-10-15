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
            # Elephant(self, game),
            Lion(self, game),
            # Lion(self, game),
            Zebra(self, game),
            # Zebra(self, game),
            Gazelle(self, game),
            # Gazelle(self, game),
        }

        self.set_pieces_to_be_placed = self.piece_set()

        self.pieces_placed = set()

        self.pieces_captured = set()

    def get_legal_moves(self, game):
        list_possible_moves = []

        for x, y in game.constants.SQUARES_INDICES_NO_CORNER:
            # Rules don't allow piece placement in the corners
            if game.board[x][y] is game.empty_square:
                for piece in self.set_pieces_to_be_placed:
                    list_possible_moves.append(("Place", x, y, piece))

        for piece in self.pieces_placed:
            list_possible_moves.extend(piece.get_legal_moves(game))

        return list_possible_moves

    def piece_set(self):
        """
        :return: a list without duplicate of the pieces_to_be_placed list
        """
        result = set()
        for piece in self.pieces_to_be_placed:
            if not any(piece.piece_id == p.piece_id for p in result):
                result.add(piece)
        return result

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


