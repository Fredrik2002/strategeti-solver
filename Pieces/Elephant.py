from Pieces.Piece import Piece
from Strategeti import Strategeti


class Elephant(Piece):

    def __init__(self, white_color):
        super().__init__("E", white_color)

    def get_legal_moves(self, board : list[list[str]]):
        list_legal_moves = []

        # Push up :
        elephant = False
        for i in range(self.x - 1, -1, -1):

            # Off board, or Elephant on the piece up
            if isinstance(board[i][self.y], Elephant):
                elephant = True
                break
            # Empty square
            elif isinstance(board[i][self.y], str):
                if i != self.x - 1:
                    break
        if not elephant and self.x - 1 >= 0 and isinstance(board[self.x - 1][self.y], Piece):
            list_legal_moves.append(("Push Up", self.x - 1, self.y, self))

        # Push down
        elephant = False
        for i in range(self.x + 1, 4):

            # Off board, or Elephant on the piece up
            if isinstance(board[i][self.y], Elephant):
                elephant = True
                break
            # Empty square
            elif isinstance(board[i][self.y], str):
                if i != self.x + 1:
                    break
        # Elephant check passed, and piece next to the elephant
        if not elephant and self.x + 1 <= 3 and isinstance(board[self.x + 1][self.y], Piece):
            list_legal_moves.append(("Push Down", self.x + 1, self.y, self))

        # Push left
        elephant = False
        for i in range(self.y - 1, -1, -1):

            # Off board, or Elephant on the piece up
            if isinstance(board[self.x][i], Elephant):
                elephant = True
                break
            # Empty square
            elif isinstance(board[self.x][i], str):
                if i != self.y - 1:
                    break
        # Elephant check passed, and piece next to the elephant
        if not elephant and self.y - 1 >= 0 and isinstance(board[self.x][self.y - 1], Piece):
            list_legal_moves.append(("Push Left", self.x, self.y - 1, self))

        # Push right
        elephant = False
        for i in range(self.y + 1, 4):

            # Off board, or Elephant on the piece up
            if isinstance(board[self.x][i], Elephant):
                elephant = True
                break
            # Empty square
            elif isinstance(board[self.x][i], str):
                if i != self.y + 1:
                    break
        # Elephant check passed, and piece next to the elephant
        if not elephant and self.y + 1 <= 3 and isinstance(board[self.x][self.y + 1], Piece):
            list_legal_moves.append(("Push Right", self.x, self.y + 1, self))

        return list_legal_moves

    def make_move(self, game : Strategeti, move : tuple[str, int , int, Piece]):
        move_name, x, y, _ = move

        if move_name == "Push Up":
            self._push_iteration(range(self.x - 1, -1, -1), [self.y] * self.x, game)

        elif move_name == "Push Down":
            self._push_iteration(range(self.x + 1, 4), [self.y] * (3 - self.x), game)

        elif move_name == "Push Left":
            self._push_iteration([self.x] * self.y, range(self.y - 1, -1, -1), game)

        elif move_name == "Push Right":
            self._push_iteration([self.x] * (3 - self.y), range(self.y + 1, 4), game)

        else:
            super().make_move(game.board, move)

    def _push_iteration(self, x_range, y_range, game : Strategeti):
        game.board[self.x][self.y] = ''

        # We start by moving the elephant
        next_piece = self
        for x, y in enumerate(x_range, y_range):
            current_piece = next_piece
            if current_piece == '':
                break
            next_piece = game.board[x][y]
            current_piece.set_coords(x, y, game)

        # If the last piece is pushed off the board
        if next_piece != '':
            next_piece.set_coords(-1, -1, game)


