from Pieces.Elephant import Elephant
from Pieces.Gazelle import Gazelle
from Pieces.Lion import Lion
from Pieces.Zebra import Zebra
from Player import Player
from PositionStorage import PositionStorage
from Strategeti import Strategeti

game = Strategeti()
player = game.player1
lion = player.get_free_piece(Lion(player))

# Case 1 : Empty board
game.make_move(("Place", 1, 2, lion))
assert lion.get_legal_moves(game.get_board()) == [], lion.get_legal_moves(game.get_board())
assert game.pieces_moved[-1] == [lion]

game.cancel_move()
assert lion.get_coords() == (-1, -1)
assert lion in player.pieces_to_be_placed
assert not lion in player.pieces_placed
assert lion.past_positions == []

# Case 2 : Pieces near, push in all 4 directions
game = Strategeti()
player = game.player1
lion = player.get_free_piece(Lion(player))
zebra = player.get_free_piece(Zebra(player))

game.make_move(("Place", 3, 1, lion))
game.make_move(("Place", 3, 0, zebra))

assert (lion.get_legal_moves(game.get_board()) ==
        [('C', 3, 0, lion)]), lion.get_legal_moves(game.get_board())
game.make_move(('C', 3, 0, lion))
assert lion.get_coords() == (3, 0)
assert zebra.get_coords() == (-1, -1)
assert zebra.is_captured
assert zebra in player.pieces_captured
assert zebra not in player.pieces_placed

game.cancel_move()
assert lion.get_coords() == (3, 1)
assert zebra.get_coords() == (3, 0)
assert not zebra.is_captured
assert not zebra in player.pieces_captured
assert zebra in player.pieces_placed
assert game.board[3][0] == zebra

