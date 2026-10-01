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
storage = PositionStorage()
init_size = 0

logging.basicConfig(level=logging.DEBUG)

# 1. We load the database if it exists
if os.path.exists("../tests/database.pkl"):
    logging.error("Loading database...")
    storage.load_database()
    init_size = len(storage.positions)
    logging.error(f"Database of {init_size} elements successfully loaded")
else:
    logging.error("Cannot find database at ../tests/database.pkl. Restarting the solving from scratch.")

# 2. We create the game instance
game = Strategeti()
game.set_database(storage)

# 3. We start the play
start = time.time()
try :
    game.play()
except (Exception, KeyboardInterrupt) as e:
    end = time.time()

    # 4. We save the database state before quitting
    logging.debug(traceback.format_exc())
    logging.error(f"Saving database : Database size : {len(storage.get_database())}, "
          f"New positions found : {len(storage.get_database()) - init_size} in {round(end - start, 3)}s")
    storage.save_database()
    logging.error("Database saved successfully")
