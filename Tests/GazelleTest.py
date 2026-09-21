from Pieces.Elephant import Elephant
from Pieces.Gazelle import Gazelle
from Pieces.Lion import Lion
from Strategeti import Strategeti
from Pieces.Zebra import Zebra

game = Strategeti()
player = game.player1
gazelle = Gazelle(player)

# Case 1 : Empty board
game.make_move(("Place", 1,2, gazelle))
assert gazelle.get_legal_moves(game.get_board()) == []

# Case 2 : Lower jump available
game.make_move(("Place", 2, 2, Zebra(player)))
assert gazelle.get_legal_moves(game.get_board()) == [('M', 3, 2, gazelle)], gazelle.get_legal_moves(game.get_board())

# Case 3 : Lower & left jump available
game.make_move(("Place", 1,1, Zebra(player)))
game.make_move(("Place", 1,3, Zebra(player)))
assert gazelle.get_legal_moves(game.get_board()) == [('M', 3, 2, gazelle), ('M', 1, 0, gazelle)]


# Case 4 : Multiple jumps
game.make_move(("Place", 2, 0, Zebra(player)))
assert gazelle.get_legal_moves(game.get_board()) == [('M', 3, 2, gazelle), ('M', 1, 0, gazelle), ('M', 3, 0, gazelle)], gazelle.get_legal_moves(game.get_board())

# Case 5
game = Strategeti()
player = game.player1
gazelle = Gazelle(player)
game.make_move(("Place", 3, 2, gazelle))
game.make_move(("Place", 2, 2, Zebra(player)))
game.make_move(("Place", 1, 2, Zebra(player)))
game.make_move(("Place", 2, 1, Zebra(player)))
assert gazelle.get_legal_moves(game.get_board()) == [('M', 0, 2, gazelle), ('M', 1, 0, gazelle)], gazelle.get_legal_moves(game.get_board())

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

assert gazelle1.get_legal_moves(game.get_board()) == []
assert gazelle2.get_legal_moves(game.get_board()) == [('M', 1, 1, gazelle2)]
game.make_move(gazelle2.get_legal_moves(game.get_board())[0])
assert gazelle2.get_coords() == (1, 1)

game.cancel_move()
assert gazelle2.get_coords() == (1, 3)


