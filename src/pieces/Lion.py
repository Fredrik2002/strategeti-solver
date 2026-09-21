from src.pieces.Piece import Piece


class Lion(Piece):
    def __init__(self, white_color):
        super().__init__("L", white_color)

    def get_legal_moves(self, board : list[list[str]]):
        list_legal_moves = []
        if self.x - 1 >= 0 and board[self.x - 1][self.y].__str__() in ['z', 'Z', 'g', 'G']:
            list_legal_moves.append(("C", self.x - 1, self.y, self))
        if self.x + 1 <= 3 and board[self.x + 1][self.y].__str__() in ['z', 'Z', 'g', 'G']:
            list_legal_moves.append(("C", self.x + 1, self.y, self))
        if self.y - 1 >= 0 and board[self.x][self.y - 1].__str__() in ['z', 'Z', 'g', 'G']:
            list_legal_moves.append(("C", self.x, self.y - 1, self))
        if self.y + 1 <= 3 and board[self.x][self.y + 1].__str__() in ['z', 'Z', 'g', 'G']:
            list_legal_moves.append(("C", self.x, self.y + 1, self))
        return list_legal_moves

    def make_move(self, game, move : tuple[str, int , int, None]):
        move_name, x, y, _ = move
        if move_name == "C":
            # A piece gets captured, we remove it from the board
            piece_captured : Piece = game.board[x][y]
            piece_captured.set_coords_and_game(-1, -1, game)

        super().make_move(game, move)
