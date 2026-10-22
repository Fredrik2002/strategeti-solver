
from src.tree_search.CompleteSearch import CompleteSearch
from src.utils.Strategeti import Strategeti

game = Strategeti(3)
tree_search = CompleteSearch()

while True:
    available_moves = game.player1.get_legal_moves(game) if game.white_to_move else game.player2.get_legal_moves(game)
    sorted_moves = []
    print(f"{'White' if game.white_to_move else 'Black'} to move : ")
    for i, move in enumerate(available_moves):
        game.make_move(move)
        fen = game.get_footprint()
        evaluation = game.search_strategy.parent_to_subpositions.get(fen)[-1]

        game.cancel_move()
        sorted_moves.append((move, evaluation))

    #     if evaluation[0] == 0 and evaluation[1] < 0:
    #         sorted_moves[0].append((move, evaluation, footprint))
    #     elif evaluation[0] == 0 and evaluation[1] > 0:
    #         sorted_moves[1].append((move, evaluation, footprint))
    #     elif evaluation[0] == -1:
    #         sorted_moves[2].append((move, evaluation, footprint))
    #     else:
    #         sorted_moves[3].append((move, evaluation, footprint))
    #
    # if game.white_to_move:
    #     sorted_moves = sorted_moves[3] + sorted(sorted_moves[1], key=lambda a : a[1][1]) \
    #     + sorted(sorted_moves[0], key=lambda a : a[1][1]) + sorted_moves[2]
    # else:
    #     sorted_moves = sorted_moves[2] + sorted(sorted_moves[0], key=lambda a: a[1][1], reverse=True) \
    #                    + sorted(sorted_moves[1], key=lambda a: a[1][1], reverse=True) + sorted_moves[3]

    for i, (move, evaluation) in enumerate(sorted_moves):
        print(f"[{i}] : {move}, {evaluation}")
    print()

    player_choice = ""
    while not player_choice.isdigit() or int(player_choice) >= len(available_moves):
        player_choice = input()
    player_choice = int(player_choice)
    game.make_move(sorted_moves[player_choice][0])
    game.show_board()
    if game.check_winner():
        print("Game is finished")
        break

