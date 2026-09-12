import json
from json import JSONDecodeError
import traceback
from PositionStorage import PositionStorage
from Strategeti import Strategeti
import os

storage = PositionStorage()

if os.path.exists("database.json"):
    with open("database.json") as f:
        try:
            database = json.loads(f.read())
            storage.set_database(database)
        except TypeError as e:
            print(e)
        except JSONDecodeError as e:
            print(e)

game = Strategeti()
game.set_database(storage)

try :
    game.play()
except Exception as e:
    print(traceback.format_exc())
    print("Database saved successfully")
    storage.save_database()
