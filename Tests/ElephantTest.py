from Pieces.Elephant import Elephant
from Pieces.Gazelle import Gazelle
from Pieces.Lion import Lion
from Player import Player
from PositionStorage import PositionStorage
from Strategeti import Strategeti

game = Strategeti()
player = game.player1
elephant = player.get_free_piece(Elephant(player))

# Case 1 : Empty board
game.make_move(("Place", 1, 2, elephant))
assert elephant.get_legal_moves(game.get_board()) == [], elephant.get_legal_moves(game.get_board())
assert game.pieces_moved[-1] == [elephant]

game.cancel_move()
assert elephant.past_positions == []
assert elephant in elephant.player.pieces_to_be_placed
assert not elephant in elephant.player.pieces_placed

# Case 2 : Pieces near, push in all 4 directions
game.make_move(("Place", 1, 2, elephant))
game.make_move(("Place", 1,1, Gazelle(player)))
game.make_move(("Place", 1,3, Gazelle(player)))
game.make_move(("Place", 0,2, Gazelle(player)))
game.make_move(("Place", 2,2, Gazelle(player)))
game.make_move(("Place", 2, 1, Gazelle(player)))

assert (elephant.get_legal_moves(game.get_board()) ==
        [('Push Up', 0, 2, elephant), ('Push Down', 2, 2, elephant),
         ('Push Left', 1, 1, elephant), ('Push Right', 1, 3, elephant)]), elephant.get_legal_moves(game.get_board())


# Case 3 : Make the move ('Push Left', 1, 1, elephant)
game.make_move(("Place", 1, 0, Lion(player)))
game.remove_piece(1, 3)

game.make_move(('Push Left', 1, 1, elephant))
assert elephant.get_coords() == (1, 1)

# Case 4 : Push row with gap in the middle
game = Strategeti()
elephant = Elephant(player)
gazelle1 = Gazelle(player)
gazelle2 = Gazelle(player)

game.make_move(("Place", 1, 3, elephant))
game.make_move(("Place", 1, 2, gazelle1))
game.make_move(("Place", 1, 0, gazelle2))

game.make_move(('Push Left', 1, 2, elephant))
assert elephant.get_coords() == (1,2)
assert gazelle1.get_coords() == (1, 1)
assert gazelle2.get_coords() == (1, 0)
assert elephant.past_positions[-1] == (1, 3)

# Case 5 : Push animal off the grid
game.make_move(('Push Left', 1, 1, elephant))
assert elephant.get_coords() == (1,1)
assert gazelle1.get_coords() == (1, 0)
assert gazelle2.get_coords() == (-1, -1), gazelle2.get_coords()
assert gazelle2.is_captured

# Case 6 : We cancel the last move, and check that all the pieces are back to their original positions
game.cancel_move()
assert elephant.get_coords() == (1,2)
assert gazelle1.get_coords() == (1, 1)
assert gazelle2.get_coords() == (1, 0), gazelle2.get_coords()
assert not gazelle2.is_captured

# Case 7 : Elephant on the same row
game = Strategeti()
elephant = Elephant(player)
game.make_move(("Place", 3, 1, elephant))
game.make_move(("Place", 2, 1, Gazelle(player)))
game.make_move(("Place", 0, 1, Elephant(player)))
game.make_move(("Place", 3, 2, Elephant(player)))
assert elephant.get_legal_moves(game.get_board()) == [("Push Up", 2, 1, elephant)], elephant.get_legal_moves(game.get_board())

# Case 8 :
game = Strategeti()
player = game.player1
elephant = player.get_free_piece(Elephant(player))
gazelle = player.get_free_piece(Gazelle(player))
game.make_move(("Place", 3, 2, elephant))
game.make_move(("Place", 3, 3, gazelle))

assert elephant.get_legal_moves(game.get_board()) == [("Push Right", 3, 3, elephant)], elephant.get_legal_moves(game.get_board())
game.make_move(("Push Right", 3, 3, elephant))
assert gazelle.get_coords() == (-1, -1)
assert elephant.get_coords() == (3, 3)
assert gazelle.is_captured
game.cancel_move()
assert gazelle.get_coords() == (3, 3)
assert elephant.get_coords() == (3, 2)
assert not gazelle.is_captured

