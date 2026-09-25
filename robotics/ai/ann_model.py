import torch
import torch.nn as nn
import torch.optim as optim

class ANNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(361, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 4)  # FORWARD, LEFT, RIGHT, STOP

    def forward(self, x):
        x = self.relu(self.fc1(x))
        return self.fc2(x)

# 1. Initialize Model, Loss, and Optimizer
model = ANNModel()
criterion = nn.CrossEntropyLoss()  # Use nn.MSELoss() if doing DQN
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 2. Dummy Training Loop Example
model.train()
for epoch in range(5):
    # Simulated batch: 32 samples, 361 features each
    inputs = torch.randn(32, 361)
    
    # Simulated ground-truth action labels (0 to 3)
    targets = torch.randint(0, 4, (32,))
    
    # Forward pass: Get action logits
    outputs = model(inputs)
    
    # Calculate loss
    loss = criterion(outputs, targets)
    
    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    print(f"Epoch {epoch+1} | Loss: {loss.item():.4f}")

# 3. Inference Example (Selecting an Action)
model.eval()
with torch.no_grad():
    state = torch.randn(1, 361)  # Single state observation
    logits = model(state)
    action_probabilities = torch.softmax(logits, dim=-1)
    predicted_action = torch.argmax(action_probabilities, dim=-1).item()
    
    actions_map = {0: "FORWARD", 1: "LEFT", 2: "RIGHT", 3: "STOP"}
    print(f"\nPredicted Action: {actions_map[predicted_action]} (Index: {predicted_action})")
