"""
The tests class to call to start the solving of the game
"""

import logging
import time
import traceback
from logging import DEBUG, ERROR

from src.utils.PositionStorage import PositionStorage
from src.utils.Strategeti import Strategeti
import os
import sys

sys.setrecursionlimit(100_000_000)
init_size = 0

logging.basicConfig(level=logging.DEBUG)



# 2. We create the game instance
game = Strategeti(3)

# 3. We start the play
start = time.time()
try :
    game.play()
except (Exception, KeyboardInterrupt) as e:


    # 4. We save the database state before quitting
    logging.error(traceback.format_exc())

end = time.time()
logging.error(f"Saving database : Database size : {len(game.position_storage.get_database())}, "
      f"New positions found : {len(game.position_storage.get_database()) - init_size} in {round(end - start, 3)}s")
game.save_storage()
logging.error("Database saved successfully")
