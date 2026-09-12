import json


class Position:
    def __init__(self, fen):
        self.fen = fen

        # True if the current position is finished (White won, Black won or draw)
        self.finished = False

        # The position in unknown
        # Evaluation = "White" <==> White won
        # Evaluation = "Black" <==> Black won
        # Evaluation = "Draw" <==> Draw
        # Evaluation = x <==> White wins in x moves
        # Evaluation = -x <==> Black wins in x moves
        self.evaluation = None



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
        with open('database.json', 'w') as f:
            f.write("{\n")

            for i, (key, value) in enumerate(self.positions.items()):
                json.dump(key, f)
                f.write(": ")
                json.dump(value, f)

                if i < len(self.positions) - 1:
                    f.write(",")

                f.write("\n")

            f.write("}\n")