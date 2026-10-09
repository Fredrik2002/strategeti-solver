from src.pieces.Piece import Piece


class EmptySquare(Piece):
    def __init__(self, player, game):
        super().__init__(" ", player, game)

    def get_legal_moves(self, board: list[list[str]]):
        return []
