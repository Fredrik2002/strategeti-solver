import datetime
import logging


class CompleteSearch:
    def __init__(self):
        pass

    def start_search(self, game, player):
        move_to_position_dict = set()
        possible_moves = player.get_legal_moves(game)

        for i, move in enumerate(possible_moves):
            game.make_move(move)

            # Unless it's a draw, We keep the game going if we don't know the evaluation of this position
            if game.draw:
                new_eval = True, 0
                move_to_position_dict.add(new_eval)
            else:
                fen = game.get_footprint()
                if fen not in game.position_storage.get_database():
                    game.play()

                new_eval = game.position_storage.get_database().get(fen)
                move_to_position_dict.add(new_eval)

            # We go back to the original position
            game.cancel_move()

        self.evaluate_and_save(game, move_to_position_dict, player)

    def evaluate_and_save(self, game, move_to_position_dict, player):
        '''
        Computes the best possible move along all the possibilities.
        The best move is used to compute the current position evaluation
        Once the best move is computed, the position evaluation is saved in the database

        :param game: The game with the original position
        :param move_to_position_dict: The correspondance move -> FEN position
        '''
        best_eval = None
        for finished, evaluation in move_to_position_dict:
            if player.white_color:
                if self.is_better_white((finished, evaluation), best_eval):
                    best_eval = finished, evaluation
            else:
                if self.is_better_black((finished, evaluation), best_eval):
                    best_eval = finished, evaluation


        game.position_storage.save_state(game, 0, self.next_eval(*best_eval, player))

    def is_better_white(self, new_eval, best_eval):
        """
        For white, ordering from worst to best is : [(1, -1), (0, -1), (0, -2),  (0, -3), ..., (1, 0), ..., (0, 3), (0, 2), (0, 1), (1, 1)]

        For black, ordering from worst to be is : [White, +1, +2, +3, ..., 0, ..., -3, -2, -1, Black]

        :return: true is evaluation is better than best_eval for the current_player
        """
        if best_eval is None : return True
        finished_new, eval_new = new_eval
        finished_best, eval_best = best_eval

        # Both positions are winning
        if eval_new > 0 and eval_best > 0:
            if eval_new == eval_best: # == 1
                return finished_new == 1
            return eval_new < eval_best

        # Both positions are losing
        elif eval_new < 0 and eval_best < 0:
            if eval_new == eval_best: # == -1
                return finished_new == 0
            return eval_new > eval_best
        else:
            return eval_new > eval_best

    def is_better_black(self, new_eval, best_eval):
        """
        For black, ordering from worst to be is : [(1, 1), (0, 1), (0, 2), (0, 3), ..., (1, 0), ..., (0, -3), (0, -2), (0, -1), (1, -1)]

        :return: true is evaluation is better than best_eval for the current_player
        """
        if best_eval is None: return True
        finished_new, eval_new = new_eval
        finished_best, eval_best = best_eval

        # Both positions are losing
        if eval_new > 0 and eval_best > 0:
            if eval_new == eval_best:  # == 1
                return finished_new == 0
            return eval_new > eval_best

        # Both positions are losing
        elif eval_new < 0 and eval_best < 0:
            if eval_new == eval_best:  # == -1
                return finished_new == 1
            return eval_new < eval_best
        else:
            return eval_new < eval_best



    def next_eval(self, finished, evaluation, player):
        # Game is finished, M1 for either white or black
        if finished == 1:
            return evaluation

        if player.white_color:
            if evaluation > 0:
                return evaluation + 1
            else:
                return evaluation
        else:
            if evaluation < 0:
                return evaluation - 1
            else:
                return evaluation
