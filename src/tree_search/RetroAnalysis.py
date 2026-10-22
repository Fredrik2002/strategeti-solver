import logging
import os
import pickle
import time
import traceback

from tqdm import tqdm


class RetroAnalysis:
    def __init__(self):
        # STEP 1 : Find all the terminated positions

        # Stores for each position, the list of its parents + its evaluation
        self.parent_to_subpositions : dict[int, tuple[list[int], list[int], tuple[int, int]]] = {0 : ([], [], None)}

        self.progress_bar_step1 = tqdm(desc="Step 1 Progression", unit="positions", total=3_719_282, position=0)

        self.progress_bar_step2 = tqdm(desc="Step 2 Progression", unit="positions", total=3_719_282, position=0)

        self.step1_done = False

    def start_search(self, game, player):
        init_size = len(self.parent_to_subpositions)
        start = time.time()
        try:
            print(f"Starting the search : Step 1 : {self.step1_done}")
            if not self.step1_done:
                print(f"Step 1 starting with initial {len(self.parent_to_subpositions)} positions")
                self.step1(game, game.player1)
                self.step1_done = True
                end = time.time()
                print(f"Step 1 completed : {len(self.parent_to_subpositions)} positions discovered in {end - start}s")
                game.search_strategy.save_database(game.filename)

            self.progress_bar_step1.close()
            print(f"Step 2 starting")
            self.step2()
        except (Exception, KeyboardInterrupt) as e:

            # 4. We save the database state before quitting
            logging.error(traceback.format_exc())

        end = time.time()
        logging.error(f"Saving database : Database size : {len(game.search_strategy.parent_to_subpositions)}, "
                      f"New positions found : {len(game.search_strategy.parent_to_subpositions) - init_size} in {round(end - start, 3)}s")
        game.search_strategy.save_database(game.filename)
        logging.error("Database saved successfully")

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
        parent = self.parent_to_subpositions[initial_fen]

        for i, move in enumerate(possible_moves):
            game.make_move(move)

            fen = game.get_footprint()
            parent[0].append(fen)

            if fen not in self.parent_to_subpositions:
                self.progress_bar_step1.update(1)

                evaluation = self.game_won(game)
                if evaluation != 0:
                    self.parent_to_subpositions[fen] = ([], [initial_fen], (evaluation, 0))
                else:
                    # Position cannot be evaluated so far, we only store the parents
                    self.parent_to_subpositions[fen] = ([], [initial_fen], None)

                    # New position to explore
                    self.step1(game, self.get_player(game))
            else:
                self.parent_to_subpositions[fen][1].append(initial_fen)

            game.cancel_move()

    # STEP 2
    def step2(self):
        queue : list[int, int, int] = [(key, *pos[-1]) for key, pos in self.parent_to_subpositions.items()
                                       if pos[-1] is not None]
        global_dtz = -1

        n_solved = len(queue)
        self.progress_bar_step2.update(n_solved)

        while queue:
            position, evaluation, dtz = queue.pop(0)

            if global_dtz < abs(dtz):
                print(f"Next distance to 0 : {abs(dtz)}")
                global_dtz = abs(dtz)

            parents = self.parent_to_subpositions[position][1]

            for parent in parents:
                if self.parent_to_subpositions[parent][-1] is not None:
                    # Position already solved
                    continue

                if evaluation > 0 and parent % 2 == 0:
                    # parent is winning for white
                    sons, p, _ = self.parent_to_subpositions[parent]
                    self.parent_to_subpositions[parent] = (sons, p, (evaluation, dtz + 1))

                    queue.append((parent, evaluation, dtz + 1))

                    n_solved += 1
                    self.progress_bar_step2.update(1)
                elif evaluation < 0 and parent % 2 == 1:
                    # parent is winning for black
                    sons, p, _ = self.parent_to_subpositions[parent]
                    self.parent_to_subpositions[parent] = (sons, p, (evaluation, dtz - 1))

                    queue.append((parent, evaluation, dtz - 1))

                    n_solved += 1
                    self.progress_bar_step2.update(1)
                else:
                    if len([p for p in self.parent_to_subpositions[parent][0] if self.parent_to_subpositions[p][2] is None]) == 0:
                        # All the subpositions are computed
                        evaluations = list(map(lambda son : self.parent_to_subpositions[son][-1],
                                               self.parent_to_subpositions[parent][0]))

                        if parent % 2 == 0:
                            new_eval = self.compute_best_eval_for_white(evaluations)
                        else:
                            new_eval = self.compute_best_eval_for_black(evaluations)

                        sons, p, _ = self.parent_to_subpositions[parent]
                        self.parent_to_subpositions[parent] = (sons, p, new_eval)
                        queue.append((parent, *new_eval))

                        n_solved += 1
                        self.progress_bar_step2.update(1)

            # Optimisation : we can clear the parents
            self.parent_to_subpositions[position] = (None, None, (evaluation, dtz))


    def compute_best_eval_for_white(self, evaluations):
        best_eval, best_dtz = evaluations[0]
        for evaluation, dtz in evaluations:
            if best_eval == 1 and evaluation == 1 and dtz < best_dtz:
                best_eval, best_dtz = evaluation, dtz
            elif best_eval == -1 and evaluation == -1 and dtz < best_dtz:
                best_eval, best_dtz = evaluation, dtz
            elif evaluation == 1 and best_eval == -1:
                best_eval, best_dtz = evaluation, dtz

        if best_eval > 0:
            return best_eval, best_dtz + 1
        else:
            return best_eval, best_dtz - 1

    def compute_best_eval_for_black(self, evaluations):
        best_eval, best_dtz = evaluations[0]
        for evaluation, dtz in evaluations:
            if best_eval == -1 and evaluation == -1 and dtz > best_dtz:
                best_eval, best_dtz = evaluation, dtz
            elif best_eval == 1 and evaluation == 1 and dtz > best_dtz:
                best_eval, best_dtz = evaluation, dtz
            elif evaluation == -1 and best_eval == +1:
                best_eval, best_dtz = evaluation, dtz

        if best_eval < 0:
            return best_eval, best_dtz - 1
        else:
            return best_eval, best_dtz + 1


    def save_database(self, filename):
        with open(filename, "wb") as f:
            pickle.dump((self.parent_to_subpositions, self.step1_done), f, protocol=pickle.HIGHEST_PROTOCOL)

    def load_database(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                logging.error("Loading database...")
                self.parent_to_subpositions, self.step1_done = pickle.load(f)
                # self.progress_bar_step1.update(len(self.parent_to_subpositions))
                init_size = len(self.parent_to_subpositions)
                logging.error(f"Database of {init_size} elements successfully loaded")
        else:
            logging.error(f"Cannot find database at {filename}. Restarting the solving from scratch.")






