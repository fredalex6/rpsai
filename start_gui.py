import tkinter as tk
from game_gui import start_game
from config import GEOMETRY


def start_menu():
    root = tk.Tk()
    root.title("RPS AI")
    root.geometry(GEOMETRY)
    root.configure(bg="white")

    # escape closes the window
    root.bind("<Escape>", lambda event: root.destroy())

    def launch_game():
        """Clear the start menu widgets and build the game screen"""
        for widget in root.winfo_children():
            widget.destroy()
        start_game(root)

    title_label = tk.Label(
        root,
        text="RPS AI",
        font=("Helvetica", 32, "bold"),
        bg="white",
    )
    title_label.pack(pady=(30, 5))

    # underline effect under the title
    underline = tk.Frame(root, bg="black", height=2, width=140)
    underline.pack(pady=(0, 20))

    description_label = tk.Label(
        root,
        text="Spill stein, saks, papir mot et nevralt nettverk!",
        font=("Helvetica", 12),
        bg="white",
        fg="gray30",
        wraplength=400,
        justify="left",
    )
    description_label.pack(pady=(0, 30))

    start_button = tk.Button(
        root,
        text="Start new game",
        font=("Helvetica", 16, "bold"),
        bg="#2ecc71",
        fg="white",
        activebackground="#27ae60",
        relief="raised",
        borderwidth=3,
        padx=20,
        pady=10,
        command=launch_game,
    )
    start_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    start_menu()