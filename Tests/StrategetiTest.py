import random
import json
from Player import Player
from PositionStorage import PositionStorage
from Strategeti import Strategeti
import os

storage = PositionStorage()

if os.path.exists("database.json"):
    with open("database.json") as f:
        database = json.loads(f)
        storage.set_database(database)

game = Strategeti(storage.get_database())

try :
    game.play()
except KeyboardInterrupt:
    print("Database saved successfully")
    storage.save_database()
