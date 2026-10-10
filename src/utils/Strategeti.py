from src.pieces.EmptySquare import EmptySquare
from src.tree_search.CompleteSearch import CompleteSearch
from src.utils import Player
from src.pieces.Piece import Piece
from src.utils.Constants import Constants


class Strategeti:
    def __init__(self, N, position_storage = None):
        self.N = N

        # We compute all the constants we will need
        self.constants = Constants(N)

        self.position_set = set()
        self.position_storage = position_storage
        self.player1 = Player.Player(self, True)
        self.player2 = Player.Player(self, False)
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

        self.search_strategy = CompleteSearch()

    def play(self):
        if self.check_winner():
            return True

        if self.white_to_move:
            self.search_strategy.start_search(self, self.player1)
        else:
            self.search_strategy.start_search(self, self.player2)

    def show_board(self):
        print(f"{'White' if self.white_to_move else 'Black'} to move")
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
            self.position_storage.save_state(self.get_footprint(), finished, evaluation)
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

    def print_footprint(self):
        res = self.footprint >> 1
        return hex(res)
