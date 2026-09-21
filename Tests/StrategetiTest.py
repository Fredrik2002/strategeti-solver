import json
from json import JSONDecodeError
import traceback
from PositionStorage import PositionStorage
from Strategeti import Strategeti
import os
import sys

sys.setrecursionlimit(100_000)
storage = PositionStorage()
init_size = 0

if os.path.exists("dataase.json"):
    with open("database.json") as f:
        try:
            database = json.loads(f.read())
            init_size = len(database)
            storage.set_database(database)
        except TypeError as e:
            print(e)
        except JSONDecodeError as e:
            print(e)

game = Strategeti()
game.set_database(storage)

try :
    game.play()
except (Exception, KeyboardInterrupt) as e:
    print(traceback.format_exc())
    print(f"Saving database : Database size : {len(storage.get_database())}, "
          f"New positions : {len(storage.get_database()) - init_size}")
    storage.save_database()
    print("Database saved successfully")
