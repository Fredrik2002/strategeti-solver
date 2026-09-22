import json
from json import JSONDecodeError
import pickle

from src.utils.PositionStorage import PositionStorage
import os
import time


storage = PositionStorage()

if os.path.exists("database.json"):
    with open("database.json") as f:
        try:
            start = time.time()
            database = json.loads(f.read())
            end = time.time()
            print(f"JSON loading time : {end-start}")
            storage.set_database(database)
        except TypeError as e:
            print(e)
        except JSONDecodeError as e:
            print(e)

with open('database.json', 'w') as f:
    start = time.time()
    json.dump(database, f)
    end = time.time()
    print(f"JSON dumping time : {end - start}")

with open("database.pkl", "rb") as f:
    start = time.time()
    database = pickle.load(f)
    end = time.time()
    print(f"Pickle loading time : {end - start}")

with open("database.pkl", "wb") as f:
    start = time.time()
    pickle.dump(database, f, protocol=pickle.HIGHEST_PROTOCOL)
    end = time.time()
    print(f"Pickle dumping time : {end - start}")

start = time.time()
for pos in ["0|GGLLZglzz|ZE___gE__e_l__e_1",
            "0|GGLLZglzz|_E__Ze___E_l__eg1",
            "1|GLLZglzz|gE__G_eZ_Eel____3",
            "1|GLLZglzz|gE__G_ez_Eel____3",
            "0|GLLZgllzz|__E__E___e_e_GgZ1"]:
    if pos in database:
        print(database[pos])
    else:
        print("Not found")
end=time.time()

print(end-start)
