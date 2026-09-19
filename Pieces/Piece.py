from abc import ABC, abstractmethod

from Strategeti import Strategeti


class Piece(ABC):
    def __init__(self, name :str, white_color : bool):
        if not white_color:
            self.name = name.lower()
        else:
            self.name = name

        self.is_captured = False

        # Piece is not yet on the board
        self.x = -1
        self.y = -1

        self.white_color = white_color
        self.id = id(self)

        self.past_positions = []


    def set_coords(self, x, y):
        self.x = x
        self.y = y
        self.past_positions.append((x, y))
        if (x, y) == (-1, -1):
            self.is_captured = True

    def set_coords(self, x, y, game : Strategeti):
        game.pieces_moved[-1].add(self)
        game.board[x][y] = self

        self.set_coords(x, y)

    def get_coords(self):
        return self.x, self.y

    @abstractmethod
    def get_legal_moves(self, board : list[list[str]]):
        pass

    def make_move(self, board : list[list[str]], move : tuple[str, int , int, None]):
        move_name, x, y, _ = move
        board[x][y] = self

        # We clear the previous position
        if move_name in ["M", "C"]:
            board[self.x][self.y] = ""
            self.past_positions.append((self.x, self.y))

        self.x, self.y = x, y

    def cancel_move(self, game):
        position = game.get_FEN_board()[:-1]
        game.position_set[position] -= 1

        # Clear the previous position
        game.board[self.x][self.y] = ""

        # Put new one on the board
        self.x, self.y = self.past_positions.pop(-1)
        game.board[self.x][self.y] = self
        game.history.pop(-1)
        game.white_to_move = not game.white_to_move

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return other.__class__ == self.__class__ and other.id == self.id

    def __hash__(self):
        return self.id