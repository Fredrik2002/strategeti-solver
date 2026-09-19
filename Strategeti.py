import random

from Pieces.Piece import Piece
import Player
from PositionStorage import PositionStorage


class Strategeti:
    def __init__(self):
        self.board = [['' for _ in range(4)] for _ in range(4)]
        self.position_set = {}
        self.database = {}
        self.player1 = Player.Player(True, self.database)
        self.player2 = Player.Player(False, self.database)
        self.draw = False
        self.white_to_move = True
        self.history = []
        self.move_number = 0
        self.pieces_moved = []

    def put_piece(self, x, y, piece : Piece):
        self.board[x][y] = piece
        piece.set_coords(x, y)

        if (x not in [0,3] or y not in [0,3]) and self.board[x][y] == '':
            self.board[x][y] = piece
            piece.set_coords(x, y)

            return True
        return False

    def remove_piece(self, x, y):
        piece = self.board[x][y]
        self.board[x][y] = ''
        return piece

    def show_board(self):
        print(self.get_FEN_board())
        print("-----------------")
        for line in self.board:
            print("|", end=' ')
            for case in line:
                if case == '':
                    case = " "
                print(case, end=" | ")
            print()
            print("-----------------")
        print()

    def play(self):
        self.move_number += 1
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
        finished = False
        evaluation = None
        if len(self.player1.pieces_captured) == 5:
            print("Black won : 5 captures")
            evaluation = "Black"
            finished = True
        elif len(self.player2.pieces_captured) == 5:
            print("White won : 5 captures")
            evaluation = "White"
            finished = True
        elif self.draw:
            print(self.get_FEN_board())
            print("Draw : 3 times repetition")
            evaluation = 0
            finished = True
        elif self.white_to_move:
            if len(self.player1.get_legal_moves(self.board)) == 0:
                print("Black won : White out of moves")
                evaluation = "Black"
                finished = True
        else:
            if len(self.player2.get_legal_moves(self.board)) == 0:
                print("White won : Black out of moves")
                evaluation = "White"
                finished = True

        if finished:
            self.database.save_state(self.get_FEN_board(), finished, evaluation)
        return finished

    def make_move_on_board(self, move):
        player = self.player1 if self.white_to_move else self.player2
        piece = move[-1]
        if move[0] == "Place":
            player.pieces_placed.append(move[-1])
            player.pieces_to_be_placed.remove(move[-1])
        piece.make_move(self.get_board(), move)

        self.white_to_move = not self.white_to_move

        self.player1.update_pieces()
        self.player2.update_pieces()

        new_position = self.get_FEN_board()[:-1]
        if new_position not in self.position_set:
            self.position_set[new_position] = 1
        else:
            self.position_set[new_position] += 1
            # If the position repeats 3 times, the game is declared draw
            if self.position_set[new_position] == 3:
                self.draw = True

        self.history.append(move)

    def get_FEN_board(self):
        """
        - 1 character : 0 -> white to move, 1 -> black to move
        - The list of to be placed pieces for both players
        - |
        - The list of captured pieces for both players
        - |
        - The board (row major, empty squares represented by underscore)
        - The number of time the position was reached


        :return:
        """
        turn = "0" if self.white_to_move else "1"
        to_be_placed_p1 = list(map(lambda piece : piece.__str__(), self.player1.pieces_to_be_placed))
        to_be_placed_p2 = list(map(lambda piece : piece.__str__(), self.player2.pieces_to_be_placed))
        placed = "".join(sorted(to_be_placed_p1 + to_be_placed_p2))

        captured_p1 = list(map(lambda piece: piece.__str__(), self.player1.pieces_captured))
        captured_p2 = list(map(lambda piece: piece.__str__(), self.player2.pieces_captured))
        captured = "".join(sorted(captured_p1 + captured_p2))

        board = []
        for row in self.board:
            for piece in row:
                if piece == '':
                    board.append("_")
                else:
                    board.append(piece.__str__())

        partial = turn + placed + "|" + captured + "|" + "".join(board)
        if partial not in self.position_set:
            return partial + "0"
        else:
            return partial + str(self.position_set[partial])

    def FEN_safety(self):
        fen = self.get_FEN_board()
        for c in ['G', 'g', 'l', 'L', 'e', 'E', 'Z', 'z']:
            assert fen.count(c) == 2

        for x in range(4):
            for y in range(4):
                if self.board[x][y] != '':
                    assert self.board[x][y].get_coords() == (x, y)


    def get_board(self):
        return self.board

    def set_database(self, database):
        self.database = database
        self.player1.position_storage = database
        self.player2.position_storage = database

    def get_database(self):
        return self.database

if __name__ == '__main__':
    main = Strategeti()
    main.put_piece(1, 2, "e")
    main.show_board()