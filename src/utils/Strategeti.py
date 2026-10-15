import logging
import os

from src.pieces.EmptySquare import EmptySquare
from src.tree_search.CompleteSearch import CompleteSearch
from src.tree_search.RetroAnalysis import RetroAnalysis
from src.utils import Player
from src.pieces.Piece import Piece
from src.utils.Constants import Constants
from src.utils.PositionStorage import PositionStorage


class Strategeti:
    def __init__(self, N):
        self.N = N

        # We compute all the constants we will need
        self.constants = Constants(N)

        self.position_set = set()
        self.player1 = Player.Player(self, True)
        self.player2 = Player.Player(self, False)
        self.nb_pieces = len(self.player1.pieces_to_be_placed)

        self.position_storage = PositionStorage()

        self.draw = False
        self.white_to_move = True
        self.history = []
        self.pieces_moved = []

        # Creates an empty square object to be placed in every
        self.empty_square = EmptySquare(self.player1, self)

        # Board flatten, row-major
        self.board = [[self.empty_square for _ in range(N)] for _ in range(N)]

        # We store the footprint to not recreating it from scratch at each move
        self.footprint = 0

        self.search_strategy = RetroAnalysis()

        self.filename = f"../tests/database_{self.N}x{self.N}_{self.nb_pieces}_pieces.pkl"
        self.load_storage()

    def play(self):
        if self.check_winner():
            return True

        if self.white_to_move:
            self.search_strategy.start_search(self, self.player1)
        else:
            self.search_strategy.start_search(self, self.player2)

    def show_board(self):
        print(f"{'White' if self.white_to_move else 'Black'} to move")
        print(f"Evaluation : {self.position_storage.get_database()[self.footprint]}")
        print(f"Footprint : {self.footprint} = {bin(self.footprint)}")
        print(f"To be placed pieces : White : {self.player1.get_to_be_placed_pieces()}, Black : {self.player2.get_to_be_placed_pieces()}")
        print(f"Captured pieces : White : {self.player1.get_captured_pieces()}, Black : {self.player2.get_captured_pieces()}")
        print("-----------------")
        for row in self.board:
            for i, case in enumerate(row):
                if i % self.N == 0:
                    print("|", end=' ')
                print(case, end=" | ")
            print()
            print("-----------------")
        print()


    def check_winner(self):
        """
        Checks if the game is over

        finished = 0 if the position is not finished
                   1 if white won
                   -1 if black won

        evaluation = 0 if the game is finished (finished != 0)

        :return: True if the game is finished (White won, Black won, or draw), False otherwise
        """
        finished = 0
        evaluation = 0
        if len(self.player1.pieces_captured) == 5:
            evaluation = -1
            finished = 1
        elif len(self.player2.pieces_captured) == 5:
            evaluation = 1
            finished = 1
        elif self.draw:
            finished = 1
            evaluation = 0
        elif self.white_to_move:
            if len(self.player1.get_legal_moves(self)) == 0:
                evaluation = -1
                finished = 1
        else:
            if len(self.player2.get_legal_moves(self)) == 0:
                evaluation = 1
                finished = 1

        if finished:
            self.position_storage.save_state(self, finished, evaluation)
        return finished or self.draw

    def make_move(self, move):
        self.pieces_moved.append([])
        piece = move[-1]
        if move[0] == "Place":
            piece.player.pieces_placed.add(move[-1])
            piece.player.pieces_to_be_placed.discard(move[-1])

            if not any(x.piece_id == piece.piece_id for x in piece.player.pieces_to_be_placed):
                piece.player.set_pieces_to_be_placed = set(filter(lambda x : x.piece_id != piece.piece_id,
                                                                  piece.player.set_pieces_to_be_placed))

        piece.make_move(self, move)

        self.white_to_move = not self.white_to_move

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
        if not self.draw:
            # We reached the position for the first time -> back to 0
            self.position_set.discard(self.get_footprint())
        else:
            # The game is draw, so reached the position for the second time -> back to 1,
            # we keep the position in the position_set
            self.draw = False

    def set_piece_on_board(self, piece, x, y):
        self.board[x][y] = piece

        self.footprint &= self.constants.CLEAR_MAPPING_INDICES_BIT[x][y]
        self.footprint |= self.constants.SET_MAPPING_INDICES_BIT[x][y][piece.piece_id - 1]

    def clear_piece_on_board(self, x, y):
        self.board[x][y] = self.empty_square

        self.footprint &= self.constants.CLEAR_MAPPING_INDICES_BIT[x][y]

    def get_footprint(self):
        return self.footprint

    def print_footprint(self, footprint=None):
        if footprint is None:
            footprint = self.footprint

        res = footprint >> 1
        board = str(hex(res)[-9:]) + str(footprint % 2)
        return board

    def recompute_footprint(self, new_board):
        """
        Function called to compute the footprint of a symmetrical position as the current board
        The symmetric board is passed as a parameter, the captured pieces are the same

        :param new_board: A symmetric version of the current board
        :return: The footprint of the new_board
        """
        result = 0

        for x in range(self.N):
            for y in range(self.N):
                piece = new_board[x][y]
                if piece is not self.empty_square:
                    result |= self.constants.SET_MAPPING_INDICES_BIT[x][y][piece.piece_id - 1]

        # We simply copy the captured pieces information, and the player's turn
        result |= self.footprint & self.constants.CAPTURED_PIECES_BITS
        return result

    def load_storage(self):
        if os.path.exists(self.filename):
            logging.error("Loading database...")
            self.search_strategy.load_database(self.filename)
            init_size = len(self.position_storage.positions)
            logging.error(f"Database of {init_size} elements successfully loaded")
        else:
            logging.error(f"Cannot find database at {self.filename}. Restarting the solving from scratch.")

    def save_storage(self):
        self.search_strategy.save_database(self.filename)


