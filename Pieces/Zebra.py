from Pieces.Piece import Piece


class Zebra(Piece):
    def __init__(self, white_color):
        super().__init__("Z", white_color)

    def get_legal_moves(self, board : list[list[str]]):
        list_legal_moves = []

        # Move to the left
        for i in range(self.x - 1, -1, -1):
            if board[i][self.y] == '':
                list_legal_moves.append(("M", i, self.y, self))
            else:
                break

        # Move to the right
        for i in range(self.x + 1, 4):
            if board[i][self.y] == '':
                list_legal_moves.append(("M", i, self.y, self))
            else:
                break

        # Move up
        for i in range(self.y - 1, -1, -1):
            if board[self.x][i] == '':
                list_legal_moves.append(("M", self.x, i, self))
            else:
                break

        # Move down
        for i in range(self.y + 1, 4):
            if board[self.x][i] == '':
                list_legal_moves.append(("M", self.x, i, self))
            else:
                break

        # Diagonal moves
        list_legal_moves.extend(self.moves_diagonal(board, -1, -1))
        list_legal_moves.extend(self.moves_diagonal(board, 1, -1))
        list_legal_moves.extend(self.moves_diagonal(board, -1, 1))
        list_legal_moves.extend(self.moves_diagonal(board, 1, 1))

        return list_legal_moves

    def moves_diagonal(self, board, x_offset, y_offset):
        list_legal_moves = []
        for coeff in range(1, 4):
            if (0 <= self.x + x_offset * coeff <= 3 and 0 <= self.y + y_offset * coeff <= 3
                    and board[self.x + x_offset* coeff][self.y + y_offset* coeff] == ''):
                list_legal_moves.append(("M", self.x + x_offset * coeff, self.y + y_offset* coeff, self))
            else:
                break
        return list_legal_moves

