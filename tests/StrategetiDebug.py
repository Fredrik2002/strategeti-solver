

from src.tree_search.CompleteSearch import CompleteSearch
from src.utils.Strategeti import Strategeti

tree_search = CompleteSearch()
game = Strategeti(3)

evaluations = {(0, 2), (0, 4), (0, 5), (0, 7)}

# print(tree_search.evaluate_and_save(game, evaluations, game.player2))

# Footprints

biggest_footprint = 0b_01_00_00_00_00_00_0000_0100_0000_0000_0000_0011_0000_0000_0000_0
game.footprint = biggest_footprint
game.position_set[biggest_footprint] = 2
print(bin(game.get_footprint_with_repetition(game.get_footprint())))