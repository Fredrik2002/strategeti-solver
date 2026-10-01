from src.pieces.EmptySquare import EmptySquare
from src.utils import Player
from src.pieces.Piece import Piece
from src.utils.Constants import MASK_POSITION_FOOTPRINT, MAPPING_INDICES_BIT, CLEAR_MAPPING_INDICES_BIT, \
    SET_MAPPING_INDICES_BIT


class Strategeti:
    def __init__(self):

        self.position_set = set()
        self.database = {}
        self.player1 = Player.Player(True, self.database)
        self.player2 = Player.Player(False, self.database)
        self.draw = False
        self.white_to_move = True
        self.history = []
        self.pieces_moved = []

        # Keeps track of all the pieces captured
        self.capture_counts = [0] * 8

        # Creates an empty square object to be placed in every
        self.empty_square = EmptySquare(self.player1)

        # Board flatten, row-major
        self.board = [[self.empty_square for _ in range(4)] for _ in range(4)]

        # We store the footprint to not recreating it from scratch at each move
        self.footprint = 0

    def play(self):
        if self.check_winner():
            return True

        if self.white_to_move:
            self.player1.make_move(self)
        else:
            self.player2.make_move(self)


    def check_winner(self):
        """
        Checks if the game is over

        :return: True if the game is finished (White won, Black won, or draw), False otherwise
        """
        finished = 0
        evaluation = None
        if len(self.player1.pieces_captured) == 5:
            evaluation = 0
            finished = -1
        elif len(self.player2.pieces_captured) == 5:
            evaluation = 0
            finished = 1
        elif self.draw:
            evaluation = 0
        elif self.white_to_move:
            if len(self.player1.get_legal_moves(self)) == 0:
                evaluation = 0
                finished = -1
        else:
            if len(self.player2.get_legal_moves(self)) == 0:
                evaluation = 0
                finished = 1

        if finished:
            self.database.save_state(self.get_footprint(), finished, evaluation)
        return finished or self.draw

    def make_move(self, move):
        self.pieces_moved.append([])
        piece = move[-1]
        if move[0] == "Place":
            piece.player.pieces_placed.add(move[-1])
            piece.player.pieces_to_be_placed.discard(move[-1])
        piece.make_move(self, move)

        self.white_to_move = not self.white_to_move

        self.player1.update_pieces()
        self.player2.update_pieces()

        self.footprint ^= 1
        self.add_position_to_set()

        self.history.append(move)

    def cancel_move(self):
        self.history.pop()

        self.remove_position_from_set()

        self.white_to_move = not self.white_to_move

        pieces_moved : list[Piece] = self.pieces_moved.pop()
        for piece_moved in pieces_moved:
            piece_moved.cancel_move(self)

        self.footprint ^= 1

    def add_position_to_set(self):
        """
        Adds a position in the position_set (or increase the count if the position was already seen)

        :return:
        """
        position = self.get_footprint()
        if position in self.position_set:
            self.draw = True
        else:
            self.position_set.add(self.get_footprint())

    def remove_position_from_set(self):
        self.draw = False
        self.position_set.discard(self.get_footprint())

    def set_piece_on_board(self, piece, x, y):
        self.board[x][y] = piece

        self.footprint &= CLEAR_MAPPING_INDICES_BIT[x][y]
        self.footprint |= SET_MAPPING_INDICES_BIT[x][y][piece.piece_id - 1]

    def clear_piece_on_board(self, x, y):
        self.board[x][y] = self.empty_square

        self.footprint &= CLEAR_MAPPING_INDICES_BIT[x][y]


    def get_footprint(self):
        return self.footprint

    def print_footprint(self):
        res = self.footprint >> 1
        return hex(res)

    def set_database(self, database):
        self.database = database
        self.player1.position_storage = database
        self.player2.position_storage = database
