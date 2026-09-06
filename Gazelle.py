from Piece import Piece


class Gazelle(Piece):

    def __init__(self, white_color):
        super().__init__("G", white_color)

    def legal_moves(self, board : list[list[str]]):
        list_legal_moves = [("M", self.x, self.y)]
        position_stack = [(self.x, self.y)]
        while len(position_stack) > 0:
            x, y = position_stack.pop()

            # The list of offsets in which a jump could be possible
            possible_jump = []
            for x_offset in range(-1, 2):
                for y_offset in range(-1, 2):
                    if 0 <= x + x_offset <= 3 and 0 <= y + y_offset <= 3:
                        if board[x + x_offset][y + y_offset] not in ['', self]:
                            # Possible jump
                            possible_jump.append((x_offset, y_offset, 2))

            while len(possible_jump) > 0:
                x_offset, y_offset, coeff = possible_jump.pop()
                if 0 <= x + x_offset * coeff <= 3 and 0 <= y + y_offset * coeff <= 3:
                    if board[x + x_offset * coeff][y + y_offset * coeff] not in ['', self]:
                        # Bigger jump possible
                        possible_jump.append((x_offset, y_offset, coeff + 1))
                    elif ("M", x + x_offset * coeff, y + y_offset * coeff) not in list_legal_moves:
                        position_stack.append((x + x_offset * coeff, y + y_offset * coeff))
                        list_legal_moves.append(("M", x + x_offset * coeff, y + y_offset * coeff))


        list_legal_moves.pop(0)
        return list_legal_moves
