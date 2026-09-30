from src.pieces.Elephant import Elephant
from src.pieces.Gazelle import Gazelle
from src.pieces.Lion import Lion
from src.utils.Strategeti import Strategeti
from src.pieces.Zebra import Zebra

game = Strategeti()
player = game.player1
gazelle = Gazelle(player)

# Case 1 : Empty board
game.make_move(("Place", 1,2, gazelle))
assert gazelle.get_legal_moves(game) == []

# Case 2 : Lower jump available
game.make_move(("Place", 2, 2, Zebra(player)))
assert gazelle.get_legal_moves(game) == [('M', 3, 2, gazelle)], gazelle.get_legal_moves(game)

# Case 3 : Lower & left jump available
game.make_move(("Place", 1,1, Zebra(player)))
game.make_move(("Place", 1,3, Zebra(player)))
assert gazelle.get_legal_moves(game) == [('M', 3, 2, gazelle), ('M', 1, 0, gazelle)]


# Case 4 : Multiple jumps
game.make_move(("Place", 2, 0, Zebra(player)))
assert gazelle.get_legal_moves(game) == [('M', 3, 2, gazelle), ('M', 1, 0, gazelle), ('M', 3, 0, gazelle)], gazelle.get_legal_moves(game)

# Case 5
game = Strategeti()
player = game.player1
gazelle = Gazelle(player)
game.make_move(("Place", 3, 2, gazelle))
game.make_move(("Place", 2, 2, Zebra(player)))
game.make_move(("Place", 1, 2, Zebra(player)))
game.make_move(("Place", 2, 1, Zebra(player)))
assert gazelle.get_legal_moves(game) == [('M', 0, 2, gazelle), ('M', 1, 0, gazelle)], gazelle.get_legal_moves(game)

# Case 6
game = Strategeti()
player = game.player1
gazelle1 = Gazelle(player)
gazelle2 = Gazelle(player)
game.make_move(("Place", 1, 2, gazelle1))
game.make_move(("Place", 1, 3, gazelle2))
game.make_move(("Place", 0, 1, Zebra(player)))
game.make_move(("Place", 0, 2, Elephant(player)))
game.make_move(("Place", 2, 0, Lion(player)))
footprint = game.get_footprint()

assert gazelle1.get_legal_moves(game) == []
assert gazelle2.get_legal_moves(game) == [('M', 1, 1, gazelle2)]
game.make_move(gazelle2.get_legal_moves(game)[0])
assert gazelle2.get_coords() == (1, 1)
assert game.footprint_ok
assert game.footprint == game.get_position_as_integer2(), (hex(game.footprint >> 1), hex(game.get_position_as_integer2() >> 1))

game.cancel_move()
assert gazelle2.get_coords() == (1, 3)
assert game.footprint == game.get_position_as_integer2(), (game.print_footprint())
assert game.footprint == footprint


