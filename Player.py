import random

from Pieces.Elephant import Elephant
from Pieces.Gazelle import Gazelle
from Pieces.Lion import Lion
from Pieces.Piece import Piece
from Pieces.Zebra import Zebra


class Player:
    def __init__(self, white_color):
        self.white_color = white_color

        self.pieces_to_be_placed = [
            Elephant(white_color),
            #Elephant(white_color),
            Lion(white_color),
            #Lion(white_color),
            Zebra(white_color),
            #Zebra(white_color),
            Gazelle(white_color),
            #Gazelle(white_color),
        ]
        self.pieces_placed = []

        self.pieces_captured = []

    def get_legal_moves(self, board):
        list_possible_moves = []
        for piece in set(self.pieces_to_be_placed):
            for x in range(4):
                for y in range(4):
                    if (x not in [0, 3] or y not in [0, 3]) and board[x][y] == '':
                        list_possible_moves.append(("Place", x, y, piece))

        for piece in self.pieces_placed:
            list_possible_moves.extend(piece.get_legal_moves(board))

        return list_possible_moves

    def _choose_move(self, board):
        """
        For now, the chosen move is random

        :return: The selected move from self.get_legal_moves()
        """
        return random.choice(self.get_legal_moves(board))

    def make_move(self, board):
        # 2. We choose a move
        move = self._choose_move(board)
        print(move)

        # 3. We make on the board the move we chose
        piece = move[-1]
        if move[0] == "Place":
            self.pieces_placed.append(move[-1])
            self.pieces_to_be_placed.remove(move[-1])
        piece.make_move(board, move)

    def update_pieces(self):
        newly_captured = [piece for piece in self.pieces_placed if piece.is_captured]
        for piece in newly_captured:
            self.pieces_placed.remove(piece)
            self.pieces_captured.append(piece)
            print(f"Piece captured : {piece}")
