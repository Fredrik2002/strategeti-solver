import pickle
import time


class Position:
    def __init__(self, fen):
        self.fen = fen
        self.subpositions = []
        self.parents = []
        self.evaluation = None

    def __eq__(self, other):
        return other.fen == self.fen

    def __str__(self):
        return f"{self.fen} : {self.evaluation}"

    def __repr__(self):
        return self.__str__()


class RetroAnalysis:
    def __init__(self):
        # STEP 1 : Find all the terminated positions

        # Stores for each position, the list of its subpositions
        self.parent_to_subpositions : dict[int, Position] = {0 : Position(0)}

        self.step1_done = False

    def start_search(self, game, player):
        print(f"Starting the search : Step 1 : {self.step1_done}")
        if not self.step1_done:
            start = time.time()
            print(f"Step 1 starting with initial {len(self.parent_to_subpositions)} positions")
            self.step1(game, game.player1)
            self.step1_done = True
            end = time.time()
            print(f"Step 1 completed : {len(self.parent_to_subpositions)} positions discovered in {end - start}s")

        print(f"Step 2 starting")
        self.step2()

    def get_player(self, game):
        return game.player1 if game.white_to_move else game.player2

    def game_won(self, game):
        if len(game.player1.pieces_captured) == 5 or \
            game.white_to_move and len(game.player1.get_legal_moves(game)) == 0:
           return -1
        elif len(game.player2.pieces_captured) == 5 or \
                not game.white_to_move and len(game.player2.get_legal_moves(game)) == 0:
            return 1
        return 0

    def step1(self, game, player):
        possible_moves = player.get_legal_moves(game)

        initial_fen = game.get_footprint()

        for i, move in enumerate(possible_moves):
            game.make_move(move)

            fen = game.get_footprint()
            self.parent_to_subpositions[initial_fen].subpositions.append(fen)

            already_seen = False
            if fen not in self.parent_to_subpositions:
                new_position = Position(fen)
                self.parent_to_subpositions[fen] = new_position
                new_position.parents.append(initial_fen)
            else:
                self.parent_to_subpositions[fen].parents.append(initial_fen)
                already_seen = True

            # Already seen = already evaluated
            if not already_seen:
                evaluation = self.game_won(game)
                if evaluation != 0:
                    self.parent_to_subpositions[fen].evaluation = (evaluation, 0)

                self.step1(game, self.get_player(game))


            game.cancel_move()

    # STEP 2
    def step2(self):
        queue = [(pos.fen, *pos.evaluation) for key, pos in self.parent_to_subpositions.items() if pos.evaluation is not None]
        on_going_positions = {}

        while queue:
            position, evaluation, dtz = queue.pop(0)

            parents = self.parent_to_subpositions[position].parents

            for parent in parents:
                if evaluation > 0 and parent % 2 == 0:
                    # parent is winning for white
                    self.parent_to_subpositions[parent].evaluation = (evaluation, dtz + 1)
                    queue.append((parent, evaluation, dtz + 1))
                elif evaluation < 0 and parent % 2 == 1:
                    # parent is winning for black
                    self.parent_to_subpositions[parent].evaluation = (evaluation, dtz - 1)
                else:
                    if len(self.parent_to_subpositions[parent]) == on_going_positions[parent]:
                        # All the subpositions are computed
                        evaluations = list(map(lambda son : self.parent_to_subpositions[son].evaluation, self.parent_to_subpositions[parent]))

                        if parent % 2 == 0:
                            new_eval = self.compute_best_eval_for_white(evaluations)
                        else:
                            new_eval = self.compute_best_eval_for_black(evaluations)
                        self.parent_to_subpositions[parent].evaluation = new_eval
                    else:
                        if parent not in on_going_positions:
                            on_going_positions[parent] = 0
                        else:
                            on_going_positions[parent] += 1

    def compute_best_eval_for_white(self, evaluations):
        best_eval, best_dtz = evaluations[0]
        for evaluation, dtz in evaluations:
            if best_eval == 1 and evaluation == 1 and dtz < best_dtz:
                best_eval, best_dtz = evaluation, dtz
            elif best_eval == -1 and evaluation == -1 and dtz > best_dtz:
                best_eval, best_dtz = evaluation, dtz
            elif evaluation == 1 and best_eval == -1:
                best_eval, best_dtz = evaluation, dtz

        if best_eval > 0:
            return best_eval, best_dtz + 1
        else:
            return best_eval, best_dtz

    def compute_best_eval_for_black(self, evaluations):
        best_eval, best_dtz = evaluations[0]
        for evaluation, dtz in evaluations:
            if best_eval == -1 and evaluation == -1 and dtz > best_dtz:
                best_eval, best_dtz = evaluation, dtz
            elif best_eval == 1 and evaluation == 1 and dtz < best_dtz:
                best_eval, best_dtz = evaluation, dtz
            elif evaluation == -1 and best_eval == +1:
                best_eval, best_dtz = evaluation, dtz

        if best_eval < 0:
            return best_eval, best_dtz - 1
        else:
            return best_eval, best_dtz





    def save_database(self, filename):
        with open(filename, "wb") as f:
            pickle.dump((self.parent_to_subpositions, self.step1_done), f, protocol=pickle.HIGHEST_PROTOCOL)

    def load_database(self, filename):
        with open(filename, "rb") as f:
            self.parent_to_subpositions, self.step1_done = pickle.load(f)






