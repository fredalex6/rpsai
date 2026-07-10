import random as rd
import subprocess

from config import ROCK, PAPIR, MOVE_NAMES, HISTORY_WINDOW, RANDOM_ROUNDS
from rps_logic import result, counter, build_input
from train import train, predict_user_move


def main():
    user_score = 0
    computer_score = 0
    c_round = 1
    history = []

    while True:
        play = input("Stein, saks eller papir? ").lower()

        if play not in MOVE_NAMES:
            continue

        user_move = MOVE_NAMES.index(play)

        current_state = build_input(history[-HISTORY_WINDOW:])

        if c_round <= RANDOM_ROUNDS:
            computer_move = rd.randint(ROCK, PAPIR)
        else:
            predicted_user_move = predict_user_move(current_state)
            computer_move = counter(predicted_user_move)

        res = result(user_move, computer_move)

        # clear console
        subprocess.run('cls', shell=True, check=False)

        if res == 1:
            user_score += 1
            print(f'You won! ({user_score}-{computer_score}) The NN chose {MOVE_NAMES[computer_move]}.')
        elif res == 0:
            print(f'It was a draw! ({user_score}-{computer_score}) The NN chose {MOVE_NAMES[computer_move]}.')
        elif res == -1:
            computer_score += 1
            print(f'You lost! ({user_score}-{computer_score}) The NN chose {MOVE_NAMES[computer_move]}.')

        history.append((user_move, computer_move, res))
        train(current_state, user_move)

        c_round += 1