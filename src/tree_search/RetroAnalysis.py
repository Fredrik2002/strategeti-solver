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
        self.parent_to_subpositions : dict[int, tuple[list[int], list[int], tuple[int, int]]] = {0 : ([], [], [], None)}

        self.progress_bar_step1 = tqdm(desc="Step 1 Progression", unit="positions", total=108_984, position=0)

        self.progress_bar_step2 = tqdm(desc="Step 2 Progression", unit="positions", total=3_719_282, position=0)

        self.final_solve = {}

        self.step1_done = False

    def start_search(self, game, player):
        init_size = len(self.parent_to_subpositions)
        start = time.time()
        try:
            print(f"Starting the search : Step 1 : {self.step1_done}")
            if not self.step1_done:
                print(f"Step 1 starting with initial {len(self.parent_to_subpositions)} positions")
                self.step1(game, game.player1)
                self.progress_bar_step1.refresh()
                self.step1_done = True
                end = time.time()
                print(f"Step 1 completed : {len(self.parent_to_subpositions)} positions discovered in {end - start}s")

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

    def compute_symmetries(self, game):
        # We also save the symmetrical positions
        # 1.
        new_board = [[game.board[x][game.N - 1 - y] for y in range(game.N)] for x in range(game.N)]
        s1 = game.recompute_footprint(new_board)
        self.parent_to_subpositions[s1] = game.footprint

        new_board = [[game.board[game.N - 1 - y][x] for y in range(game.N)] for x in range(game.N)]
        s2 = game.recompute_footprint(new_board)
        self.parent_to_subpositions[s2] = game.footprint

        # 2.
        new_board = [[game.board[game.N - 1 - x][y] for y in range(game.N)] for x in range(game.N)]
        s3 = game.recompute_footprint(new_board)
        self.parent_to_subpositions[s3] = game.footprint

        new_board = [[game.board[y][game.N - 1 - x] for y in range(game.N)] for x in range(game.N)]
        s4 = game.recompute_footprint(new_board)
        self.parent_to_subpositions[s4] = game.footprint

        # 3. Diagonal (0, 0) stays in place
        new_board = [[game.board[y][x] for y in range(game.N)] for x in range(game.N)]
        s5 = game.recompute_footprint(new_board)
        self.parent_to_subpositions[s5] = game.footprint

        # 4.
        new_board = [[game.board[game.N - 1 - y][game.N - 1 - x] for y in range(game.N)] for x in range(game.N)]
        s6 = game.recompute_footprint(new_board)
        self.parent_to_subpositions[s6] = game.footprint

        new_board = [[game.board[game.N - 1 - x][game.N - 1 - y] for y in range(game.N)] for x in range(game.N)]
        s7 = game.recompute_footprint(new_board)
        self.parent_to_subpositions[s7] = game.footprint

        return {s1, s2, s3, s4, s5, s6, s7}


    def step1(self, game, player):
        possible_moves = player.get_legal_moves(game)

        initial_fen = game.get_footprint()
        parent = self.parent_to_subpositions[initial_fen]

        for i, move in enumerate(possible_moves):
            game.make_move(move)

            fen = game.get_footprint()
            parent[0].append(fen)

            if fen not in self.parent_to_subpositions:

                evaluation = self.game_won(game)
                if evaluation != 0:
                    size_before = len(self.parent_to_subpositions)

                    # We cannot store the symmetries because we want to have one object for all
                    self.parent_to_subpositions[fen] = ([], [initial_fen], self.compute_symmetries(game), (evaluation, 0))

                    size_after = len(self.parent_to_subpositions)

                    self.progress_bar_step1.update(size_after - size_before)
                else:
                    # Position cannot be evaluated so far, we only store the parents
                    self.parent_to_subpositions[fen] = ([], [initial_fen], self.compute_symmetries(game), None)

                    # New position to explore
                    self.step1(game, self.get_player(game))
            else:
                representative = self.parent_to_subpositions[fen]
                representative = self.parent_to_subpositions[representative] if isinstance(representative, int) else representative

                if initial_fen not in representative[1]:
                    representative[1].append(initial_fen)

            game.cancel_move()

    # STEP 2
    def compute_queue(self):
        pass

    def step2(self):

        queue : list[int, int, int] = [(key, *pos[-1]) for key, pos in self.parent_to_subpositions.items()
                                       if isinstance(pos, tuple) and pos[-1] is not None]
        super_queue = [queue]

        for fen, evaluation, dtz in queue:
            self.final_solve[fen] = (evaluation, dtz)
            for sym in self.parent_to_subpositions[fen][2]:
                self.final_solve[sym] = (evaluation, dtz)

        global_dtz = 0

        n_solved = len(queue)
        print(f"Number of solved positions : {n_solved}")
        self.progress_bar_step2.update(n_solved)

        while super_queue[global_dtz]:
            queue = super_queue[global_dtz]
            print(f"Next DTZ : {abs(global_dtz)}")
            while queue:
                for i in range(global_dtz):
                    assert super_queue[i] == []
                if super_queue[-1]:
                    super_queue.extend([[] for _ in range(10)])

                position, evaluation, dtz = queue.pop(0)

                parents = self.parent_to_subpositions[position][1]

                for parent in parents:
                    if parent in self.final_solve:
                        # Position already solved
                        continue

                    value = self.parent_to_subpositions[parent]

                    representative = parent if isinstance(value, tuple) else value

                    if not self.compute_straightly_winning(representative, evaluation, dtz, super_queue):
                        self.compute_with_all_subpositions(representative, super_queue)

                # Optimisation : we can clear the parents
                self.parent_to_subpositions.pop(position)

            global_dtz += 1

    def compute_straightly_winning(self, representative, evaluation, dtz, super_queue):
        if evaluation > 0 and representative % 2 == 0:
            # parent is winning for white
            sons, p, syms, _ = self.parent_to_subpositions[representative]

            self.parent_to_subpositions[representative] = (sons, p, syms, (evaluation, dtz + 1))

            self.final_solve[representative] = (evaluation, dtz + 1)
            for sym in self.parent_to_subpositions[representative][2]:
                # To be stored only once
                self.final_solve[sym] = (evaluation, dtz + 1)

            super_queue[dtz + 1].append((representative, evaluation, dtz + 1))

            self.progress_bar_step2.update(1)
            return True

        elif evaluation < 0 and representative % 2 == 1:
            # parent is winning for black
            sons, p, syms, _ = self.parent_to_subpositions[representative]
            self.parent_to_subpositions[representative] = (sons, p, syms, (evaluation, dtz - 1))

            self.final_solve[representative] = (evaluation, dtz - 1)
            for sym in self.parent_to_subpositions[representative][2]:
                # To be stored only once
                self.final_solve[sym] = (evaluation, dtz - 1)

            super_queue[abs(dtz) + 1].append((representative, evaluation, dtz - 1))
            self.progress_bar_step2.update(1)
            return True
        return False

    def compute_with_all_subpositions(self, representative, super_queue):
        if len([p for p in self.parent_to_subpositions[representative][0] if p not in self.final_solve]) == 0:
            # All the subpositions are computed
            evaluations = list(map(lambda son: self.final_solve[son],
                                   self.parent_to_subpositions[representative][0]))
            if representative % 2 == 0:
                new_eval, new_dtz = self.compute_best_eval_for_white(evaluations)
            else:
                new_eval, new_dtz = self.compute_best_eval_for_black(evaluations)

            sons, p, syms, _ = self.parent_to_subpositions[representative]
            self.parent_to_subpositions[representative] = (sons, p, syms, (new_eval, new_dtz))

            self.final_solve[representative] = new_eval, new_dtz
            for sym in self.parent_to_subpositions[representative][2]:
                # To be stored only once -> mapping to integer
                self.final_solve[sym] = new_eval, new_dtz

            super_queue[abs(new_dtz)].append((representative, new_eval, new_dtz))

            self.progress_bar_step2.update(1)

##################################################
####### STEP 3 : DROP DRAW POSITIONS #############
##################################################
    def step3(self):
        pass

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
            pickle.dump((self.parent_to_subpositions, self.final_solve, self.step1_done), f, protocol=pickle.HIGHEST_PROTOCOL)

    def load_database(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                logging.error("Loading database...")
                self.parent_to_subpositions, self.final_solve, self.step1_done = pickle.load(f)
                # self.progress_bar_step1.update(len(self.parent_to_subpositions))
                init_size = len(self.parent_to_subpositions)
                logging.error(f"Database of {init_size} elements successfully loaded")
        else:
            logging.error(f"Cannot find database at {filename}. Restarting the solving from scratch.")






