import torch
import torch.nn as nn
import random as rd
import subprocess

class RPSNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(45, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 3)
        )

    def forward(self, x):
        return self.network(x)


model = RPSNet()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.005
)

criterion = nn.CrossEntropyLoss()

# --- Replay buffer, so we train on more than just the single latest round ---
buffer_X = []
buffer_y = []

def train(X, y, batch_size=16, epochs=3, min_buffer=8):
    """Store this round's example, then train on random mini-batches
    sampled from everything seen so far."""
    buffer_X.append(X.squeeze(0))
    buffer_y.append(y.item())

    if len(buffer_X) < min_buffer:
        return

    for _ in range(epochs):
        k = min(batch_size, len(buffer_X))
        idx = rd.sample(range(len(buffer_X)), k)
        batch_X = torch.stack([buffer_X[i] for i in idx])
        batch_y = torch.tensor([buffer_y[i] for i in idx], dtype=torch.long)

        optimizer.zero_grad()
        prediction = model(batch_X)
        loss = criterion(prediction, batch_y)
        loss.backward()
        optimizer.step()


user_score = 0
computer_score = 0
c_round = 1

ROCK = 0
SCISSORS = 1
PAPIR = 2

history = []

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

def one_hot(move):
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

def build_input(history, n_rounds=5):

    recent = history[-n_rounds:]

    state = []

    for my_move, opp_move, outcome in recent:

        state.extend(one_hot(my_move))
        state.extend(one_hot(opp_move))

        if outcome == 1:
            state.extend([1,0,0])
        elif outcome == 0:
            state.extend([0,1,0])
        else:
            state.extend([0,0,1])

    while len(recent) < n_rounds:
        state = [0]*9 + state
        recent.insert(0, None)

    return torch.tensor([state], dtype=torch.float32)


while True:

    alt = ["stein", "saks", "papir"]
    play = input("Stein, saks eller papir? ").lower()

    if play not in alt:
        continue

    user_move = alt.index(play)
    computer_move = 0

    current_state = build_input(history[-5:])

    if c_round <= 5:
        computer_move = rd.randint(ROCK, PAPIR)
    else:
        with torch.no_grad():
            logits = model(current_state)

        predicted_user_move = logits.argmax(dim=1).item()
        computer_move = counter(predicted_user_move)


    res = result(user_move, computer_move)

    # clear console
    subprocess.run('cls', shell=True, check=False)

    if res == 1:
        user_score += 1
        print(f'You won! ({user_score}-{computer_score}) The NN chose {alt[computer_move]}.')
    elif res == 0:
        print(f'It was a draw! ({user_score}-{computer_score}) The NN chose {alt[computer_move]}.')
    elif res == -1:
        computer_score += 1
        print(f'You lost! ({user_score}-{computer_score}) The NN chose {alt[computer_move]}.')


    history.append((user_move, computer_move, res))
    train(current_state, torch.tensor([user_move]))

    c_round += 1