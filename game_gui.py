import tkinter as tk
import random as rd

from config import ROCK, SCISSORS, PAPIR, HISTORY_WINDOW, RANDOM_ROUNDS
from rps_logic import result, counter, build_input
from train import train, predict_user_move

MOVE_NAMES_NO = {ROCK: "Stein", SCISSORS: "Saks", PAPIR: "Papir"}
MOVE_EMOJIS = {ROCK: "🪨", SCISSORS: "✂️", PAPIR: "📄"}

RESULT_DELAY_MS = 800

WIN_COLOR = "#2ecc71"
LOSS_COLOR = "#e74c3c"
DRAW_COLOR = "#f1c40f"


class RPSGame:
    """GUI state for one play session"""

    def __init__(self, root):
        self.root = root
        self.root.title("RPS AI")
        self.root.geometry("500x400")

        self.user_score = 0
        self.computer_score = 0
        self.c_round = 1
        self.history = []

        # swappable container frame
        self.container = tk.Frame(self.root, bg="white")
        self.container.pack(fill="both", expand=True)

        self.show_move_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_move_screen(self):
        self.clear_container()
        self.container.configure(bg="white")

        score_label = tk.Label(
            self.container,
            text=f"{self.user_score} - {self.computer_score}",
            font=("Helvetica", 30, "bold"),
            bg="white",
        )
        score_label.pack(pady=(30, 10))

        instruction_label = tk.Label(
            self.container,
            text="Velg ditt trekk!",
            font=("Helvetica", 16),
            bg="white",
            fg="gray30",
        )
        instruction_label.pack(pady=(0, 30))

        button_frame = tk.Frame(self.container, bg="white")
        button_frame.pack()

        for move in (ROCK, SCISSORS, PAPIR):
            btn = tk.Button(
                button_frame,
                text=f"{MOVE_EMOJIS[move]}\n{MOVE_NAMES_NO[move]}",
                font=("Helvetica", 20),
                width=6,
                height=3,
                bg="#f0f0f0",
                activebackground="#dcdcdc",
                relief="raised",
                borderwidth=2,
                command=lambda m=move: self.play_round(m),
            )
            btn.pack(side="left", padx=12)

    def play_round(self, user_move):
        current_state = build_input(self.history[-HISTORY_WINDOW:])

        if self.c_round <= RANDOM_ROUNDS:
            computer_move = rd.randint(ROCK, PAPIR)
        else:
            predicted_user_move = predict_user_move(current_state)
            computer_move = counter(predicted_user_move)

        res = result(user_move, computer_move)

        if res == 1:
            self.user_score += 1
        elif res == -1:
            self.computer_score += 1

        self.history.append((user_move, computer_move, res))
        train(current_state, user_move)
        self.c_round += 1

        self.show_result_screen(user_move, computer_move, res)

    def show_result_screen(self, user_move, computer_move, res):
        self.clear_container()

        if res == 1:
            bg_color, message = WIN_COLOR, "Du vant!"
        elif res == -1:
            bg_color, message = LOSS_COLOR, "Du tapte!"
        else:
            bg_color, message = DRAW_COLOR, "Uavgjort!"

        self.container.configure(bg=bg_color)

        message_label = tk.Label(
            self.container,
            text=message,
            font=("Helvetica", 28, "bold"),
            bg=bg_color,
            fg="white",
        )
        message_label.pack(pady=(35, 15))

        moves_label = tk.Label(
            self.container,
            text=f"Du {MOVE_EMOJIS[user_move]}      vs      {MOVE_EMOJIS[computer_move]} NN",
            font=("Helvetica", 36),
            bg=bg_color,
        )
        moves_label.pack(pady=15)

        score_label = tk.Label(
            self.container,
            text=f"{self.user_score} - {self.computer_score}",
            font=("Helvetica", 18, "bold"),
            bg=bg_color,
            fg="white",
        )
        score_label.pack(pady=(15, 0))

        # automatically return to the move screen after a short pause
        self.root.after(RESULT_DELAY_MS, self.show_move_screen)


def start_game(root):
    """Build the game UI inside an existing root window"""
    root.bind("<Escape>", lambda: root.destroy())
    RPSGame(root)
