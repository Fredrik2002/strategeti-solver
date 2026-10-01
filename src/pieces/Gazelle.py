from src.pieces.Piece import Piece
from src.utils.Constants import NEIGHBOOR


class Gazelle(Piece):

    def __init__(self, white_color):
        super().__init__("G", white_color)

    def get_legal_moves(self, game):
        board = game.board
        list_legal_moves = []
        visited = {(self.x, self.y)}
        position_stack = [(self.x, self.y)]

        while position_stack:
            x, y = position_stack.pop()

            # The list of offsets in which a jump could be possible
            for n1, n2, n3 in NEIGHBOOR[x][y]:

                # The 3 neighboors, when going in direction (x_offset, y_offset) from (x, y)
                # n1 and n2 are garanteed to be not None (otherwise, no jump possible)
                p1, p2 = board[n1[0]][n1[1]], board[n2[0]][n2[1]]


                # You can't jump over empty squares, nor yourself
                if p1 is not game.empty_square and p1 is not self:
                    # Jump is possible
                    if p2 is game.empty_square and n2 not in visited:
                        # Square must be empty
                        # 2 squares jump
                        position_stack.append(n2)
                        list_legal_moves.append(("M", *n2, self))
                        visited.add(n2)
                    elif p2 is not self and p2 is not game.empty_square and n3 is not None and n3 not in visited:

                        p3 = board[n3[0]][n3[1]]
                        # 3 squares jump

                        if p3 is game.empty_square:
                            position_stack.append(n3)
                            list_legal_moves.append(("M", *n3, self))
                            visited.add(n3)

        return list_legal_moves
