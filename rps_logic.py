import torch

from config import ROCK, SCISSORS, PAPIR, HISTORY_WINDOW


def result(my_move, opp_move):
    if my_move == opp_move:
        return 0

    if (
        (my_move == ROCK and opp_move == SCISSORS) or
        (my_move == SCISSORS and opp_move == PAPIR) or
        (my_move == PAPIR and opp_move == ROCK)
    ):
        return 1

    return -1


def format(move):
    v = [0, 0, 0]
    v[move] = 1
    return v


def counter(move):
    if move == ROCK:
        return PAPIR
    elif move == PAPIR:
        return SCISSORS
    elif move == SCISSORS:
        return ROCK


def build_input(history, n_rounds=HISTORY_WINDOW):
    recent = history[-n_rounds:]

    state = []

    for my_move, opp_move, outcome in recent:
        state.extend(format(my_move))
        state.extend(format(opp_move))

        if outcome == 1:
            state.extend([1, 0, 0])
        elif outcome == 0:
            state.extend([0, 1, 0])
        else:
            state.extend([0, 0, 1])

    while len(recent) < n_rounds:
        state = [0] * 9 + state
        recent.insert(0, None)

    return torch.tensor([state], dtype=torch.float32)