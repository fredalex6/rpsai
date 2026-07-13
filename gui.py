import tkinter as tk

from game import main as start_game
from config import FONT


def start_window():
    root = tk.Tk()
    root.title("RPS AI")
    root.geometry("800x450")
    root.configure(bg="white")

    # escape closes the window
    root.bind("<Escape>", lambda event: root.destroy())

    title_label = tk.Label(
        root,
        text="RPS AI",
        font=(FONT, 32, "bold"),
        bg="white",
    )
    title_label.pack(pady=(30, 5))

    # underline effect under the title
    underline = tk.Frame(root, bg="black", height=2, width=140)
    underline.pack(pady=(0, 20))


    description_label = tk.Label(
        root,
        text="Spill 'Stein, saks, papir' mot et nevralt nett som prøve å predikere dine neste trekk",
        font=(FONT, 12),
        bg="white",
        fg="gray30",
        wraplength=400,
        justify="left",
    )
    description_label.pack(pady=(0, 30))


    start_button = tk.Button(
        root,
        text="Start new game",
        font=(FONT, 16, "bold"),
        bg="#2ecc71",
        fg="white",
        activebackground="#27ae60",
        relief="raised",
        borderwidth=3,
        padx=20,
        pady=10,
        command=lambda: (root.destroy(), start_game()),
    )
    start_button.pack(pady=25)

    root.mainloop()