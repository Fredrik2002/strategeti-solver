import pickle

class PositionStorage:
    def __init__(self):
        # Key : FEN position
        # Value : (finished, evaluation)
        self.positions = {}

    def save_state(self, fen, finished, evaluation):
        self.positions[fen] = (finished, evaluation)

    def set_database(self, database):
        self.positions = database

    def get_database(self):
        return self.positions

    def save_database(self):
        with open("../test/database.pkl", "wb") as f:
            pickle.dump(self.positions, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load_database(self):
        with open("../test/database.pkl", "rb") as f:
            self.positions = pickle.load(f)