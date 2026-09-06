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

    @abstractmethod
    def legal_moves(self, board : list[list[str]]):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()