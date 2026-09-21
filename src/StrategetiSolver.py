"""
The test class to call to start the solving of the game
"""

import json
import pickle
from json import JSONDecodeError
import traceback
from src.utils.PositionStorage import PositionStorage
from src.utils.Strategeti import Strategeti
import os
import sys

sys.setrecursionlimit(100_000_000)
storage = PositionStorage()
init_size = 0

# 1. We load the database if it exists
if os.path.exists("../test/database.pkl"):
    print("Loading database...")
    storage.load_database()
    init_size = len(storage.positions)
    print(f"Database of {init_size} elements successfully loaded")
else:
    print("Cannot find database at ../test/database.pkl. Restarting the solving from scratch.")

# 2. We create the game instance
game = Strategeti()
game.set_database(storage)

# 3. We start the play
try :
    game.play()
except (Exception, KeyboardInterrupt) as e:
    # 4. We save the database state before quitting
    print(traceback.format_exc())
    print(f"Saving database : Database size : {len(storage.get_database())}, "
          f"New positions : {len(storage.get_database()) - init_size}")
    storage.save_database()
    print("Database saved successfully")
