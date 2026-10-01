from abc import ABC, abstractmethod

from src.utils.Constants import MAPPING_INDICES_BIT, MAPPING_PIECE_INTEGER, FOOTPRINT_BIT_SHIFT


class Piece(ABC):
    def __init__(self, name : str, player):
        if not player.get_color():
            self.name = name.lower()
        else:
            self.name = name

        self.piece_id = MAPPING_PIECE_INTEGER[self.name]
        self.capture_bit_shift = (1 << FOOTPRINT_BIT_SHIFT[self.name]) if self.name in FOOTPRINT_BIT_SHIFT else -1
        self.is_captured = False

        # Piece is not yet on the board
        self.x = -1
        self.y = -1

        self.player = player
        self.id = id(self)

        self.past_positions = []


    def set_coords(self, x, y):
        self.past_positions.append((self.x, self.y))
        self.x, self.y = x, y

        self.is_captured = (x == -1 and y == -1)

    def set_coords_and_game(self, x, y, game):
        game.pieces_moved[-1].append(self)

        if (x, y) != (-1, -1):
            game.set_piece_on_board(self, x, y)
        else:
            game.footprint += self.capture_bit_shift

        self.set_coords(x, y)

    def get_coords(self):
        return self.x, self.y

    @abstractmethod
    def get_legal_moves(self, game):
        pass

    def make_move(self, game, move : tuple[str, int , int, None]):
        move_name, x, y, _ = move

        game.set_piece_on_board(self, x, y)

        game.pieces_moved[-1].append(self)

        # We clear the previous position
        if move_name in ["M", "C"]:
            game.clear_piece_on_board(self.x, self.y)

        self.past_positions.append((self.x, self.y))
        self.x, self.y = x, y

    def cancel_move(self, game):

        x, y = self.past_positions.pop()

        # Past position was off the board : The piece has been placed
        if (x, y) == (-1,-1):
            # The piece was just placed on the board
            self.player.pieces_placed.pop()
            self.player.pieces_to_be_placed.add(self)

            # We cancel the placement of the piece
            game.clear_piece_on_board(self.x, self.y)

        # Current position is off the board : Means the piece has been captured
        elif (self.x, self.y) == (-1, -1):
            assert self.is_captured

            self.player.pieces_captured.discard(self)
            self.player.pieces_placed.add(self)
            self.is_captured = False

            # We put back the piece at its original position (before the capture)
            game.set_piece_on_board(self, x, y)
            game.footprint -= self.capture_bit_shift
        else:
            # The piece was moved

            # The clear the last position, and set the new one
            if game.board[self.x][self.y] == self:
                game.clear_piece_on_board(self.x, self.y)

            game.set_piece_on_board(self, x, y)

        self.x, self.y = x, y

    def get_piece_id(self):
        return self.piece_id

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return other.__class__ == self.__class__ and other.id == self.id

    def __hash__(self):
        return self.id