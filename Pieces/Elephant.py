from Pieces.Piece import Piece


class Elephant(Piece):

    def __init__(self, white_color):
        super().__init__("E", white_color)

    def get_legal_moves(self, board : list[list[str]]):
        list_legal_moves = []
        if self.x - 1 >= 0 and board[self.x - 1][self.y] != '':
            list_legal_moves.append(("Push Up", self.x - 1, self.y, self))
        if self.x + 1 <= 3 and board[self.x + 1][self.y] != '':
            list_legal_moves.append(("Push Down", self.x + 1, self.y, self))
        if self.y - 1 >= 0 and board[self.x][self.y - 1] != '':
            list_legal_moves.append(("Push Left", self.x, self.y - 1, self))
        if self.y + 1 <= 3 and board[self.x][self.y + 1] != '':
            list_legal_moves.append(("Push Right", self.x, self.y + 1, self))
        return list_legal_moves

    def make_move(self, board : list[list[Piece]], move : tuple[str, int , int, Piece]):
        move_name, x, y, _ = move
        if "Push" in move_name:
            next_piece = board[self.x][self.y]
            board[self.x][self.y] = ''
            if move_name == "Push Up":
                for i in range(self.x - 1, -1, -1):
                    current_piece = next_piece
                    if current_piece == '':
                        break
                    next_piece = board[i][y]
                    board[i][y] = current_piece
                    current_piece.set_coords(i, y)

            elif move_name == "Push Down":
                for i in range(self.x + 1, 4):
                    current_piece = next_piece
                    if current_piece == '':
                        break
                    next_piece = board[i][y]
                    board[i][y] = current_piece
                    current_piece.set_coords(i, y)

            elif move_name == "Push Left":
                for i in range(self.y - 1, -1, -1):
                    current_piece = next_piece
                    if current_piece == '':
                        break
                    next_piece = board[x][i]
                    board[x][i] = current_piece
                    current_piece.set_coords(x, i)

            elif move_name == "Push Right":
                for i in range(self.y + 1, 4):
                    current_piece = next_piece
                    if current_piece == '':
                        break
                    next_piece = board[x][i]
                    board[x][i] = current_piece
                    current_piece.set_coords(x, i)

            if next_piece != '':
                next_piece.set_coords(-1, -1)
                next_piece.is_captured = True
        else:
            super().make_move(board, move)



