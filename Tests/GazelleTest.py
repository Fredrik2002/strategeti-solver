from Gazelle import Gazelle
from Strategeti import Strategeti
from Zebra import Zebra

game = Strategeti()
gazelle = Gazelle(True)

# Case 1 : Empty board
game.put_piece(1,2, gazelle)
assert gazelle.legal_moves(game.get_board()) == []

# Case 2 : Lower jump available
game.put_piece(2, 2, Zebra(True))
assert gazelle.legal_moves(game.get_board()) == [('M', 3, 2)], gazelle.legal_moves(game.get_board())

# Case 3 : Lower & left jump available
game.put_piece(1,1, Zebra(True))
game.put_piece(1,3, Zebra(True))
assert gazelle.legal_moves(game.get_board()) == [('M', 3, 2), ('M', 1, 0)]


# Case 4 : Multiple jumps
game.put_piece(2, 0, Zebra(True))
assert gazelle.legal_moves(game.get_board()) == [('M', 3, 2), ('M', 1, 0), ('M', 3, 0)], gazelle.legal_moves(game.get_board())

# Case 5
game = Strategeti()
gazelle = Gazelle(True)
game.put_piece(3, 2, gazelle)
game.put_piece(2, 2, Zebra(True))
game.put_piece(1, 2, Zebra(True))
game.put_piece(2, 1, Zebra(True))
assert gazelle.legal_moves(game.get_board()) == [('M', 0, 2), ('M', 1, 0)], gazelle.legal_moves(game.get_board())


