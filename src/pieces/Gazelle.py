from src.pieces.Piece import Piece


class Gazelle(Piece):

    def __init__(self, white_color):
        super().__init__("G", white_color)

    def get_legal_moves(self, board : list[list[str]]):
        list_legal_moves = []
        visited = {(self.x, self.y)}
        position_stack = [(self.x, self.y)]

        while position_stack:
            x, y = position_stack.pop()

            # The list of offsets in which a jump could be possible
            possible_jump = []
            for x_offset in range(-1, 2):
                for y_offset in range(-1, 2):
                    new_x, new_y = x + x_offset, y + y_offset
                    if 0 <= new_x <= 3 and 0 <= new_y <= 3:
                        piece = board[new_x][new_y]
                        if piece is not None and piece is not self:
                            # Possible jump
                            possible_jump.append((x_offset, y_offset, 2))

            while possible_jump:
                x_offset, y_offset, coeff = possible_jump.pop()

                new_x, new_y = x + x_offset * coeff, y + y_offset * coeff

                if 0 <= new_x <= 3 and 0 <= new_y <= 3:
                    piece = board[new_x][new_y]
                    if piece is not None and piece is not self:
                        # Bigger jump possible
                        possible_jump.append((x_offset, y_offset, coeff + 1))
                    elif (new_x, new_y) not in visited:
                        position_stack.append((new_x, new_y))
                        list_legal_moves.append(("M", new_x, new_y, self))
                        visited.add((new_x, new_y))


        return list_legal_moves
