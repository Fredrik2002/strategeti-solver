

from src.tree_search.CompleteSearch import CompleteSearch
from src.utils.Strategeti import Strategeti
import pickle

with open("database_3x3_4_pieces.pkl", "rb") as f:
    db1 = pickle.load(f)[0]
    print(len(db1))

with open("database_3x3_4_pieces2.pkl", "rb") as f:
    db2 = pickle.load(f)[0]
    print(len(db2))

db2_minus_db1 = {}
db1_minus_db2 = {}

for key, value in db1.items():
    if key not in db2 or set(db2[key][0]) != set(value[0]):
        db2_minus_db1[key] = value

for key, value in db2.items():
    if key not in db1 or set(db1[key][0]) != set(value[0]):
        db1_minus_db2[key] = value

print(len(db2_minus_db1))
print(len(db1_minus_db2))
