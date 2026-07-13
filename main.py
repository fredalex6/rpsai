from gui import start_window

if __name__ == "__main__":
    try:
        start_window()
    except KeyboardInterrupt:
        print("\nAvslutter. Takk for spillet!")
    