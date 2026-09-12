import random

from Pieces.Piece import Piece
import Player


class Strategeti:
    def __init__(self, database):
        self.board = [['' for _ in range(4)] for _ in range(4)]
        self.position_set = {}
        self.player1 = Player.Player(True, database)
        self.player2 = Player.Player(False, database)
        self.draw = False
        self.white_to_move = True
        self.database = database

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
        while True:
            self.player1.update_pieces()
            self.player2.update_pieces()

            if self.check_winner():
                break

            self.show_board()
            print(self.player1.get_legal_moves(self.board))
            if len(self.player1.get_legal_moves(self.board)) > 0:
                self.make_move(self.player1)
                self.white_to_move = False
            else:
                print("Black won : White out of moves")
                break

            self.player1.update_pieces()
            self.player2.update_pieces()

            if self.check_winner():
                break

            self.show_board()
            print(self.player2.get_legal_moves(self.board))
            if len(self.player2.get_legal_moves(self.board)) > 0:
                self.make_move(self.player2)
                self.white_to_move = True
            else:
                print("White won : Black out of moves")
                break

    def check_winner(self):
        """
        Checks if the game is over

        :return: True if the game is finished (White won, Black won, or draw), False otherwise
        """
        if len(self.player1.pieces_captured) == 5:
            print("Black won : 5 captures")
        elif len(self.player2.pieces_captured) == 5:
            print("White won : 5 captures")
        elif self.draw:
            print(self.get_FEN_board())
            print("Draw : 3 times repetition")
        else:
            return False
        return True

    def make_move(self, player):
        player.make_move(self.board)
        new_position = self.get_FEN_board()[:-1]
        if new_position not in self.position_set:
            self.position_set[new_position] = 1
        else:
            self.position_set[new_position] += 1
            # If the position repeats 3 times, the game is declared draw
            if self.position_set[new_position] == 3:
                self.draw = True

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
        to_be_placed_p1 = "".join(list(map(lambda piece : piece.__str__(), self.player1.pieces_to_be_placed)))
        to_be_placed_p2 = "".join(list(map(lambda piece : piece.__str__(), self.player2.pieces_to_be_placed)))

        captured_p1 = "".join(list(map(lambda piece: piece.__str__(), self.player1.pieces_captured)))
        captured_p2 = "".join(list(map(lambda piece: piece.__str__(), self.player2.pieces_captured)))

        board = []
        for row in self.board:
            for piece in row:
                if piece == '':
                    board.append("_")
                else:
                    board.append(piece.__str__())

        partial = turn + to_be_placed_p1 + to_be_placed_p2 + "|" + captured_p1 + captured_p2 + "|" + "".join(board)
        if partial not in self.position_set:
            return partial + "0"
        else:
            return partial + str(self.position_set[partial])


    def get_board(self):
        return self.board

if __name__ == '__main__':
    main = Strategeti()
    main.put_piece(1, 2, "e")
    main.show_board()