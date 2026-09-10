from abc import abstractclassmethod, ABC, abstractmethod


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


    '''
    Returns a list of legal moves with a 3-tuple :
    - "M" for move, "C" for capture, "P" for push
    - x : the new x coordinate for the piece
    - y : the new y coordinate for the piece
    '''

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def get_coords(self):
        return self.x, self.y

    @abstractmethod
    def get_legal_moves(self, board : list[list[str]]):
        pass

    def make_move(self, board : list[list[str]], move : tuple[str, int , int, None]):
        move_name, x, y, _ = move
        board[x][y] = self

        # We clear the previous position
        if move_name == "M":
            board[self.x][self.y] = ""

        self.x, self.y = x, y

        self.custom_make_move()

    def custom_make_move(self):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return other.__class__ == self.__class__

    def __hash__(self):
        return 0