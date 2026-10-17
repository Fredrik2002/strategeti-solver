"""
The tests class to call to start the solving of the game
"""

import logging
import sys
import time

from src.utils.Strategeti import Strategeti

sys.setrecursionlimit(100_000_000)
init_size = 0

logging.basicConfig(level=logging.DEBUG)


# 2. We create the game instance
game = Strategeti(3)

# 3. We start the play
start = time.time()
game.play()

