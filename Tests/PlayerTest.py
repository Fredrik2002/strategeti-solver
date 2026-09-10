from Player import Player
from Strategeti import Strategeti

player = Player(True)
game = Strategeti()

print(player.get_legal_moves(game.get_board()))
