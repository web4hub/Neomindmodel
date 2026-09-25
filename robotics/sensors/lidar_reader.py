import torch
import numpy as np
import time

# --- Your Sensor Mock Functions ---
def read_lidar():
    return np.random.rand(360).tolist()  # 360 degrees LiDAR

def read_distance():
    return np.random.rand(1)[0]  # distance sensor mock

def read_imu():
    return np.random.rand(1)[0]  # IMU angle mock

def get_sensor_vector():
    lidar = read_lidar()
    distance = read_distance()
    # If you want to include IMU (making it 362 dims), you'd add it here:
    # imu = read_imu()
    # return np.array(lidar + [distance, imu], dtype=np.float32)
    
    return np.array(lidar + [distance], dtype=np.float32)


# --- Model Definition (From Previous Step) ---
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


# --- Real-Time Control Loop Simulation ---
if __name__ == "__main__":
    # Initialize model
    model = AdvancedSensorReflex(input_dim=361, output_dim=4)
    model.eval()  # Set to evaluation mode for inference

    print("Starting Autonomous Reflex Loop...")
    
    try:
        for step in range(3):  # Simulate 3 control cycles
            # 1. Read hardware sensors
            raw_sensors = get_sensor_vector()  # Shape: (361,)
            
            # 2. Convert to PyTorch tensor and add a batch dimension -> Shape: (1, 361)
            sensor_tensor = torch.tensor(raw_sensors, dtype=torch.float32).unsqueeze(0)
            
            # 3. Forward pass (compute reflex commands)
            with torch.no_grad():
                motor_commands = model(sensor_tensor).squeeze(0).numpy() # Shape: (4,)
            
            # 4. Map outputs to actuator meanings
            throttle, steering, capture_trigger, aux = motor_commands
            
            print(f"\n[Cycle {step+1}]")
            print(f"  -> Throttle: {throttle:.2f}")
            print(f"  -> Steering: {steering:.2f}")
            print(f"  -> Capture Trigger: {capture_trigger:.2f}")
            print(f"  -> Aux Actuator: {aux:.2f}")
            
            time.sleep(0.5)  # Simulate control loop tick (e.g., 20Hz)
            
    except KeyboardInterrupt:
        print("Loop terminated by user.")

def read_lidar():
    # Replace with actual LiDAR library read
    return np.random.rand(360).tolist()  # 360 degrees LiDAR

def read_distance():
    return np.random.rand(1)[0]  # distance sensor mock

def read_imu():
    return np.random.rand(1)[0]  # IMU angle mock

def get_sensor_vector():
    lidar = read_lidar()
    distance = read_distance()
    return np.array(lidar + [distance], dtype=np.float32)

