import pickle

class PositionStorage:
    def __init__(self):
        # Key : FEN position
        # Value : (finished, evaluation)
        self.positions = {}

    def save_state(self, game, finished, evaluation):
        self.positions[game.get_footprint()] = (finished, evaluation)

        # We also save the symmetrical positions
        # 1. Left to right symmetry
        new_board = [[game.board[x][game.N - 1 - y] for y in range(game.N)] for x in range(game.N)]
        self.positions[game.recompute_footprint(new_board)] = (finished, evaluation)

        # 2. Up to down
        new_board = [[game.board[game.N - 1 - x][y] for y in range(game.N)] for x in range(game.N)]
        self.positions[game.recompute_footprint(new_board)] = (finished, evaluation)

        # 3. Diagonal (0, 0) stays in place
        new_board = [[game.board[y][x] for y in range(game.N)] for x in range(game.N)]
        self.positions[game.recompute_footprint(new_board)] = (finished, evaluation)

        # 4. Diagonal (0, 0) goes to (2, 2)
        new_board = [[game.board[game.N - 1 - y][game.N - 1 - x] for y in range(game.N)] for x in range(game.N)]
        self.positions[game.recompute_footprint(new_board)] = (finished, evaluation)

    def set_database(self, database):
        self.positions = database

    def get_database(self):
        return self.positions

    def save_database(self):
        with open("../tests/database.pkl", "wb") as f:
            pickle.dump(self.positions, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load_database(self):
        with open("../tests/database.pkl", "rb") as f:
            self.positions = pickle.load(f)