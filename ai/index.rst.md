# **🗂 Neurobot Starter Package Structure**

```bash
Neurobot/
│
├── arduino/
│   └── motor_control.ino       # Arduino sketch for motors/servos
│
├── sensors/
│   ├── lidar_reader.py         # LiDAR reading & preprocessing
│   ├── camera_reader.py        # Camera capture & preprocessing
│   └── imu_reader.py           # IMU & distance sensor integration
│
├── ai/
│   ├── ann_model.py            # ANN strategic decision module
│   ├── snn_model.py            # Reflexive SNN module
│   ├── rl_trainer.py           # DQN / PPO training loop
│   └── config.py               # Model & sensor config
│
├── swarm/
│   └── mqtt_comm.py            # Swarm communication via MQTT
│
├── main.py                     # Integration script, sensor → AI → motors
├── requirements.txt            # Python dependencies
└── README.md                   # Setup instructions
```

---

# **1️⃣ Arduino Motor Control** (`arduino/motor_control.ino`)

```cpp
#include <Servo.h>

Servo leftMotor, rightMotor;

void setup() {
  leftMotor.attach(9);
  rightMotor.attach(10);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    String action = Serial.readStringUntil('\n');
    if (action == "FORWARD") {
      leftMotor.write(180);
      rightMotor.write(0);
    } else if (action == "LEFT") {
      leftMotor.write(0);
      rightMotor.write(0);
    } else if (action == "RIGHT") {
      leftMotor.write(180);
      rightMotor.write(180);
    } else if (action == "STOP") {
      leftMotor.write(90);
      rightMotor.write(90);
    }
  }
}
```

---

# **2️⃣ ANN Strategic Model** (`ai/ann_model.py`)

```python
import torch
import torch.nn as nn

class ANNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(361, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 4)  # FORWARD, LEFT, RIGHT, STOP

    def forward(self, x):
        x = self.relu(self.fc1(x))
        return self.fc2(x)
```

---

# **3️⃣ SNN Reflex Module** (`ai/snn_model.py`)

```python
import torch
import torch.nn as nn

class ReflexSNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(361, 3)  # LiDAR + distance → motor spike commands

    def forward(self, x):
        return torch.sigmoid(self.fc(x))  # 0-1 motor intensity
```

---

# **4️⃣ Sensor Readers**

### **LiDAR + Distance + IMU** (`sensors/lidar_reader.py`)

```python
import numpy as np

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
```

### **Camera Reader** (`sensors/camera_reader.py`)

```python
import cv2
from torchvision import transforms
import torch

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

cap = cv2.VideoCapture(0)

def read_camera():
    ret, frame = cap.read()
    if not ret:
        return None
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return transform(frame).unsqueeze(0)  # batch dim
```

---

# **5️⃣ Swarm Communication** (`swarm/mqtt_comm.py`)

```python
import paho.mqtt.client as mqtt

MQTT_BROKER = "192.168.1.100"
client = mqtt.Client("neurobot01")
client.connect(MQTT_BROKER)

def publish_state(position, obstacles):
    msg = f"{position[0]},{position[1]},{position[2]};{obstacles}"
    client.publish("neurobot/swarm", msg)
```

---

# **6️⃣ Main Integration Script** (`main.py`)

```python
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
```

---

# **7️⃣ Dependencies** (`requirements.txt`)

```
torch
torchvision
numpy
opencv-python
paho-mqtt
```

---

# ✅ **How to Run**

1. **Upload Arduino sketch** to your Arduino Mega / Uno.
2. **Connect sensors & LiDAR to Pi/Jetson**.
3. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the Neurobot**:

```bash
python main.py
```

* The ANN will make **strategic decisions**, SNN handles **reflex motor actions**, and MQTT updates **swarm status**.
* Reward-based learning adapts the ANN over time.

---

