import torch
import torch.nn as nn

class AdvancedSensorReflex(nn.Module):
    def __init__(self, input_dim: int = 361, hidden_dim: int = 256, output_dim: int = 4):
        super().__init__()
        self.feature_extractor = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU()
        )
        self.control_head = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.GELU(),
            nn.Linear(64, output_dim),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        return self.control_head(self.feature_extractor(x))
