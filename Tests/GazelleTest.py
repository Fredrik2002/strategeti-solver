import sys

print(sys.path)

from Pieces.Elephant import Elephant
from Pieces.Gazelle import Gazelle
from Pieces.Lion import Lion
from Strategeti import Strategeti
from Pieces.Zebra import Zebra

import sys

sys.path.append("C:\\Users\\calve\\Documents\\Programming\\Python\\Strategeti")
game = Strategeti()
gazelle = Gazelle(True)

# Case 1 : Empty board
game.put_piece(1,2, gazelle)
assert gazelle.get_legal_moves(game.get_board()) == []

# Case 2 : Lower jump available
game.put_piece(2, 2, Zebra(True))
assert gazelle.get_legal_moves(game.get_board()) == [('M', 3, 2, gazelle)], gazelle.get_legal_moves(game.get_board())

# Case 3 : Lower & left jump available
game.put_piece(1,1, Zebra(True))
game.put_piece(1,3, Zebra(True))
assert gazelle.get_legal_moves(game.get_board()) == [('M', 3, 2, gazelle), ('M', 1, 0, gazelle)]


# Case 4 : Multiple jumps
game.put_piece(2, 0, Zebra(True))
assert gazelle.get_legal_moves(game.get_board()) == [('M', 3, 2, gazelle), ('M', 1, 0, gazelle), ('M', 3, 0, gazelle)], gazelle.get_legal_moves(game.get_board())

# Case 5
game = Strategeti()
gazelle = Gazelle(True)
game.put_piece(3, 2, gazelle)
game.put_piece(2, 2, Zebra(True))
game.put_piece(1, 2, Zebra(True))
game.put_piece(2, 1, Zebra(True))
assert gazelle.get_legal_moves(game.get_board()) == [('M', 0, 2, gazelle), ('M', 1, 0, gazelle)], gazelle.get_legal_moves(game.get_board())

# Case 6
print("Case 6 : ")
game = Strategeti()
gazelle1 = Gazelle(True)
gazelle2 = Gazelle(True)
game.put_piece(1, 2, gazelle1)
game.put_piece(1, 3, gazelle2)
game.put_piece(0, 1, Zebra(True))
game.put_piece(0, 2, Elephant(True))
game.put_piece(2, 0, Lion(True))
game.show_board()
assert gazelle1.get_legal_moves(game.get_board()) == []
assert gazelle2.get_legal_moves(game.get_board()) == [('M', 1, 1, gazelle2)]
gazelle2.make_move(game.get_board(), gazelle2.get_legal_moves(game.get_board())[0])
assert gazelle2.get_coords() == (1, 1)
game.show_board()


