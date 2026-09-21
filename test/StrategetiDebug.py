import copy

from src.pieces.Elephant import Elephant
from src.pieces.Gazelle import Gazelle
from src.utils.Strategeti import Strategeti

game = Strategeti()

elephant = Elephant(game.player1)
gazelle = Gazelle(game.player1)

L1 = [elephant, gazelle]
L2 = [gazelle, elephant]

assert sorted(L1) == sorted(L2)