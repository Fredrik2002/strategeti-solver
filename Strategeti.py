from Piece import Piece


class Strategeti:
    def __init__(self):
        self.board = [['' for _ in range(4)] for _ in range(4)]

    def put_piece(self, x, y, piece : Piece):
        self.board[x][y] = piece
        piece.set_coords(x, y)

        if (x not in [0,3] or y not in [0,3]) and self.board[x][y] == '':
            self.board[x][y] = piece
            piece.set_coords(x, y)

            return True
        return False

    def show_board(self):
        for line in self.board:
            print("|", end=' ')
            for case in line:
                if case == '':
                    case = " "
                print(case, end=" | ")
            print()
            print("-----------------")

    def get_board(self):
        return self.board

if __name__ == '__main__':
    main = Strategeti()
    main.put_piece(1, 2, "e")
    main.show_board()