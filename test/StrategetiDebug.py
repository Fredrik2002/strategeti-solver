import copy

from src.utils.Strategeti import Strategeti

game = Strategeti()

game2 = copy.deepcopy(game)

assert id(game.player1.pieces_to_be_placed[0]) != id(game2.player1.pieces_to_be_placed[0])