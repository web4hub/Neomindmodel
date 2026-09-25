import paho.mqtt.client as mqtt
import json
import time

class SwarmCommsNode:
    def __init__(self, client_id="neurobot01", broker_ip="192.168.1.100"):
        self.client_id = client_id
        self.client = mqtt.Client(client_id)
        
        # Bind callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        print(f"Connecting [{client_id}] to MQTT Broker at {broker_ip}...")
        self.client.connect(broker_ip, 1883, 60)
        self.client.loop_start()
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[{self.client_id}] Connected to MQTT Broker successfully!")
            client.subscribe("neurobot/swarm/#")
        else:
            print(f"[{self.client_id}] Connection failed with code {rc}")
            
    def on_message(self, client, userdata, msg):
        """Parses incoming JSON telemetry from other swarm nodes."""
        payload = msg.payload.decode('utf-8')
        try:
            data = json.loads(payload)
            sender_id = data.get("robot_id", "unknown")
            if sender_id != self.client_id:
                battery = data.get("health", {}).get("battery_level", "N/A")
                errors = data.get("health", {}).get("error_codes", [])
                print(f"[Swarm Inbound] {sender_id} | Battery: {battery}% | Errors: {errors}")
        except json.JSONDecodeError:
            pass  # Handle non-JSON text gracefully
            
    def publish_telemetry(self, position, obstacles, battery_level: float, camera_status: str, error_codes: list):
        """
        Publishes an enriched telemetry payload with position, sensors, 
        and hardware health states.
        """
        data = {
            "robot_id": self.client_id,
            "timestamp": time.time(),
            "position": list(position),          # e.g., [X, Y, Heading]
            "obstacles": list(obstacles),        # Proximity data
            "health": {
                "battery_level": float(battery_level),     # Percentage (0-100)
                "camera_status": str(camera_status),       # "OK", "DEGRADED", "OFFLINE"
                "error_codes": list(error_codes)           # e.g., [] or ["ERR_CAM_TIMEOUT"]
            }
        }
        
        msg = json.dumps(data)
        self.client.publish("neurobot/swarm/telemetry", msg)
        
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

# --- Example Usage in a Control Loop ---
if __name__ == "__main__":
    node = SwarmCommsNode(client_id="neurobot01")
    
    # Simulate a routine telemetry broadcast cycle
    try:
        for _ in range(3):
            dummy_position = (12.5, 4.2, 90.0)
            dummy_obstacles = [0.5, 1.2, 0.3]
            
            # Health metrics
            battery = 87.4                # 87.4% remaining
            cam_status = "OK"             # Camera operational
            errors = []                   # No active errors
            
            node.publish_telemetry(
                position=dummy_position, 
                obstacles=dummy_obstacles, 
                battery_level=battery, 
                camera_status=cam_status, 
                error_codes=errors
            )
            
            time.sleep(1.0)
            
    except KeyboardInterrupt:
        node.disconnect()
