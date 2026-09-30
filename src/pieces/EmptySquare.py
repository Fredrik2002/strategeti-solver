from src.pieces.Piece import Piece


class EmptySquare(Piece):
    def __init__(self, player):
        super().__init__(" ", player)

    def get_legal_moves(self, board: list[list[str]]):
        return []
