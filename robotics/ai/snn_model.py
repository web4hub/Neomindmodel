import torch
import torch.nn as nn

class AdvancedSensorReflex(nn.Module):
    """
    Advanced multi-modal reflex network for autonomous navigation and object interaction.
    
    Inputs (Combined State Vector):
        - Directional Proximity (Front, Back, Left, Right)
        - Object Analysis Features (Classification/Metrics)
        - Analog Movement Feedback (Telemetry/Encoders)
        
    Outputs (Continuous Control - 0 to 1):
        - Throttle / Forward-Backward Speed
        - Steering / Turning Angle
        - Gripper / Object Capture Trigger
        - Status / Auxiliary Actuator
    """
    def __init__(self, input_dim: int = 361, hidden_dim: int = 256, output_dim: int = 4):
        super().__init__()
        
        # Deep feature extraction to analyze object characteristics and spatial surroundings
        self.feature_extractor = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU()
        )
        
        # Motor and action control head (Analog continuous outputs)
        self.control_head = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.GELU(),
            nn.Linear(64, output_dim),
            nn.Sigmoid()  # Squashes all control signals into smooth 0-1 analog ranges
        )
        
    def forward(self, sensor_telemetry: torch.Tensor) -> torch.Tensor:
        """
        Forward pass taking unified sensor/telemetry data and outputting reflex actions.
        """
        features = self.feature_extractor(sensor_telemetry)
        control_signals = self.control_head(features)
        return control_signals

# Example Verification:
if __name__ == "__main__":
    model = AdvancedSensorReflex()
    
    # Simulate a combined batch of sensory inputs (Batch size: 4, Features: 361)
    # Includes Front/Back/Left/Right sensors, object analysis, and analog motion data
    dummy_sensors = torch.randn(4, 361)
    
    actions = model(dummy_sensors)
    
    print("Analog Control Outputs Shape:", actions.shape)  # torch.Size([4, 4])
    print("Sample Output (Throttle, Steering, Capture, Aux):\n", actions[0])
