import torch
import torch.nn as nn
import serial

class NeurobotANN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(361, 128)
        self.fc2 = nn.Linear(128, 4)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))

ser = serial.Serial('/dev/ttyUSB0', 115200)
model = NeurobotANN()
model.eval()

actions = ["FORWARD", "LEFT", "RIGHT", "STOP"]

while True:
    state = torch.rand((1, 361))
    with torch.no_grad():
        logits = model(state)
        action_idx = torch.argmax(logits, dim=-1).item()
    
    action = actions[action_idx]
    ser.write((action + "\n").encode())
