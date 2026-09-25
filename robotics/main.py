import serial
import torch
import numpy as np
from ai.ann_model import ANNModel
from ai.snn_model import ReflexSNN
from sensors.lidar_reader import get_sensor_vector
from sensors.camera_reader import read_camera
from swarm.mqtt_comm import publish_state

# Serial to Arduino
ser = serial.Serial('/dev/ttyUSB0', 115200)
actions = ["FORWARD", "LEFT", "RIGHT", "STOP"]

# Initialize models
ann_model = ANNModel()
snn_model = ReflexSNN()
optimizer = torch.optim.Adam(ann_model.parameters(), lr=0.001)
criterion = torch.nn.MSELoss()

try:
    while True:
        # Sensor vector
        sensor_vec = torch.tensor([get_sensor_vector()])
        
        # ANN decision
        ann_output = ann_model(sensor_vec)
        action_idx = torch.argmax(ann_output).item()
        action = actions[action_idx]
        
        # SNN reflex
        reflex_output = snn_model(sensor_vec).detach().numpy()
        
        # Send action to Arduino
        ser.write((action + "\n").encode())
        
        # Reward & learning
        reward = 1 if sensor_vec[0, -1] > 0.1 else -1
        target = torch.zeros_like(ann_output)
        target[0, action_idx] = reward
        optimizer.zero_grad()
        loss = criterion(ann_output, target)
        loss.backward()
        optimizer.step()
        
        # Swarm update
        position = [0,0,0]  # Replace with odometry
        publish_state(position, sensor_vec[0, :-1].tolist())
        
        print(f"Action: {action}, Reward: {reward}, Reflex: {reflex_output}")

except KeyboardInterrupt:
    print("Shutting down Neurobot")
    ser.close()
