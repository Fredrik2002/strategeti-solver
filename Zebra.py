from Piece import Piece


class Zebra(Piece):
    def __init__(self, white_color):
        super().__init__("Z", white_color)

    def legal_moves(self, board : list[list[str]]):
        list_legal_moves = []

        # Straight line moves
        for i in range(4):
            if board[i][self.y] == '':
                list_legal_moves.append((i, self.y))
            if board[self.x][i] == '':
                list_legal_moves.append((self.x, i))

        # Diagonal moves
        list_legal_moves.extend(self.moves_diagonal(-1, -1))
        list_legal_moves.extend(self.moves_diagonal(1, -1))
        list_legal_moves.extend(self.moves_diagonal(-1, 1))
        list_legal_moves.extend(self.moves_diagonal(1, 1))

        return list_legal_moves

    def moves_diagonal(self, x_offset, y_offset):
        list_legal_moves = []
        for coeff in range(1, 4):
            if 0 <= self.x + x_offset <= 3 and 0 <= self.y + y_offset <= 3:
                list_legal_moves.append(("M", x_offset, y_offset))
            else:
                break
        return list_legal_moves