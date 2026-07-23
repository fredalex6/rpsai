import torch
import torch.nn as nn

from config import BUFFER_SIZE, EPOCHS_PER_ROUND, LEARNING_RATE
from model import RPSNet

model = RPSNet()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
criterion = nn.CrossEntropyLoss()

buffer_X = []
buffer_y = []


def train(state, user_move):
    """Store this round's (state, actual user move) in a sliding-window buffer"""
    buffer_X.append(state.squeeze(0))
    buffer_y.append(user_move)

    if len(buffer_X) > BUFFER_SIZE:
        buffer_X.pop(0)
        buffer_y.pop(0)

    if len(buffer_X) <= 5:
        return

    all_X = torch.stack(buffer_X)
    all_y = torch.tensor(buffer_y, dtype=torch.long)

    for _ in range(EPOCHS_PER_ROUND):
        optimizer.zero_grad()
        prediction = model(all_X)
        loss = criterion(prediction, all_y)
        loss.backward()
        optimizer.step()


def predict_user_move(state):
    """Return the network's best guess at the user's move (argmax over logits)."""
    with torch.no_grad():
        logits = model(state)
    return logits.argmax(dim=1).item()