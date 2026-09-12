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
        self.positions = {}

    def set_database(self, database):
        self.positions = database

    def get_database(self):
        return self.positions

    def save_database(self):
        with open('database.json', 'w') as f:
            json.dump(self.positions, f)