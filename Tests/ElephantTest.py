from Pieces.Elephant import Elephant
from Pieces.Gazelle import Gazelle
from Pieces.Lion import Lion
from Strategeti import Strategeti

game = Strategeti()
elephant = Elephant(True)

# Case 1 : Empty board
game.put_piece(1, 2, elephant)
assert elephant.get_legal_moves(game.get_board()) == []

# Case 2 : Pieces near, push left & up
game.put_piece(1,1, Gazelle(True))
game.put_piece(1,3, Gazelle(True))
game.put_piece(0,2, Gazelle(True))
game.put_piece(2,2, Gazelle(True))
game.put_piece(2, 1, Gazelle(True))

assert (elephant.get_legal_moves(game.get_board()) ==
        [('Push Down', 2, 2, elephant), ('Push Left', 1, 1, elephant)]), elephant.get_legal_moves(game.get_board())


# Case 3 : Make the move ('Push Left', 1, 1, elephant)
game.put_piece(1, 0, Lion(True))
game.remove_piece(1, 3)

game.show_board()
elephant.make_move(game.get_board(), ('Push Left', 1, 1, elephant))
assert elephant.get_coords() == (1, 1)

# Case 4 : Push row with gap in the middle
game = Strategeti()
elephant = Elephant(True)
gazelle1 = Gazelle(True)
gazelle2 = Gazelle(True)

game.put_piece(1, 3, elephant)
game.put_piece(1, 2, gazelle1)
game.put_piece(1, 0, gazelle2)

game.show_board()
elephant.make_move(game.get_board(), ('Push Left', 1, 2, elephant))
assert elephant.get_coords() == (1,2)
assert gazelle1.get_coords() == (1, 1)
assert gazelle2.get_coords() == (1, 0)

# Case 5 : Push animal off the grid
elephant.make_move(game.get_board(), ('Push Left', 1, 1, elephant))
assert elephant.get_coords() == (1,1)
assert gazelle1.get_coords() == (1, 0)
assert gazelle2.get_coords() == (-1, -1), gazelle2.get_coords()
assert gazelle2.is_captured

# Case 6 : Elephant on the same row
game = Strategeti()
elephant = Elephant(True)
game.put_piece(3, 1, elephant)
game.put_piece(2, 1, Gazelle(True))
game.put_piece(0, 1, Elephant(True))
game.put_piece(3, 2, Elephant(True))
assert elephant.get_legal_moves(game.get_board()) == [("Push Up", 2, 1, elephant)], elephant.get_legal_moves(game.get_board())

