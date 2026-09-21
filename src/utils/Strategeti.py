from src.utils import Player
from src.pieces.Piece import Piece


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
        self.pieces_moved = []

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
        self.FEN_safety()
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
            # print("Black won : 5 captures")
            evaluation = "Black"
            finished = True
        elif len(self.player2.pieces_captured) == 5:
            # print("White won : 5 captures")
            evaluation = "White"
            finished = True
        elif self.draw:
            # print("Draw : 3 times repetition")
            evaluation = 0
            finished = True
        elif self.white_to_move:
            if len(self.player1.get_legal_moves(self.board)) == 0:
                # print("Black won : White out of moves")
                evaluation = "Black"
                finished = True
        else:
            if len(self.player2.get_legal_moves(self.board)) == 0:
                # print("White won : Black out of moves")
                evaluation = "White"
                finished = True

        if finished:
            self.database.save_state(self.get_FEN_board(), finished, evaluation)
        return finished

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

        self.add_position_to_set()

        self.history.append(move)

    def cancel_move(self):
        self.history.pop()

        self.remove_position_from_set()

        self.white_to_move = not self.white_to_move

        pieces_moved : list[Piece] = self.pieces_moved.pop()
        for piece_moved in pieces_moved:
            piece_moved.cancel_move(self)

    def add_position_to_set(self):
        """
        Adds a position in the position_set (or increase the count if the position was already seen)

        :return:
        """
        position = self.get_FEN_board()[:-1]
        if position not in self.position_set:
            self.position_set[position] = 1
        else:
            self.position_set[position] += 1
            # If the position repeats 3 times, the game is declared draw
            if self.position_set[position] == 3:
                self.draw = True

    def remove_position_from_set(self):
        self.draw = False
        position = self.get_FEN_board()[:-1]
        if position not in self.position_set:
            print(f"WARNING : Trying to remove position {position} from {self.history}. This should not happen.")
        elif self.position_set[position] == 1:
            self.position_set.pop(position)
        else:
            self.position_set[position] -= 1


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