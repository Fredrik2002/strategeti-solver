from src.pieces.Piece import Piece
from src.utils.Constants import ZEBRA_DIAGS


class Zebra(Piece):
    def __init__(self, white_color):
        super().__init__("Z", white_color)

    def get_legal_moves(self, game):
        board = game.board
        list_legal_moves = []

        # Move to the left
        for i in range(self.x - 1, -1, -1):
            if board[i][self.y] is game.empty_square:
                list_legal_moves.append(("M", i, self.y, self))
            else:
                break

        # Move to the right
        for i in range(self.x + 1, 4):
            if board[i][self.y] is game.empty_square:
                list_legal_moves.append(("M", i, self.y, self))
            else:
                break

        # Move up
        for i in range(self.y - 1, -1, -1):
            if board[self.x][i] is game.empty_square:
                list_legal_moves.append(("M", self.x, i, self))
            else:
                break

        # Move down
        for i in range(self.y + 1, 4):
            if board[self.x][i] is game.empty_square:
                list_legal_moves.append(("M", self.x, i, self))
            else:
                break

        # Diagonal moves
        for diagonal in ZEBRA_DIAGS[self.x][self.y]:
            for x, y in diagonal:
                if board[x][y] is game.empty_square:
                    list_legal_moves.append(("M", x, y, self))
                else:
                    # We go to the next diagonal
                    break

        return list_legal_moves

