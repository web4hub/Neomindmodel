import paho.mqtt.client as mqtt
import paho.mqtt.client as mqtt
import json

class SwarmCommsNode:
    def __init__(self, client_id="neurobot01", broker_ip="192.168.1.100"):
        self.client_id = client_id
        # Note: If using newer paho-mqtt versions (v2.0+), you may need:
        # client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
        self.client = mqtt.Client(client_id)
        
        # Bind callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        print(f"Connecting [{client_id}] to MQTT Broker at {broker_ip}...")
        self.client.connect(broker_ip, 1883, 60)
        
        # Start background network thread
        self.client.loop_start()
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[{self.client_id}] Successfully connected to MQTT Broker!")
            # Subscribe to swarm channel to hear other bots
            client.subscribe("neurobot/swarm/#")
        else:
            print(f"[{self.client_id}] Connection failed with code {rc}")
            
    def on_message(self, client, userdata, msg):
        """Callback when another robot or sensor node publishes data."""
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        if not topic.endswith(self.client_id):  # Ignore own messages
            print(f"[Swarm Inbound] From {topic}: {payload}")
            
    def publish_state(self, position, obstacles):
        """Publishes structured telemetry using JSON for robust cross-bot parsing."""
        data = {
            "robot_id": self.client_id,
            "position": list(position),
            "obstacles": obstacles
        }
        # JSON formatting is safer and easier to scale than comma/semicolon strings
        msg = json.dumps(data)
        self.client.publish("neurobot/swarm/state", msg)
        
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

# --- Example Usage ---
if __name__ == "__main__":
    node = SwarmCommsNode(client_id="neurobot01")
    
    # Simulate broadcasting state
    dummy_position = (12.5, 4.2, 90.0)  # X, Y, Heading
    dummy_obstacles = [0.5, 1.2, 0.3]   # Nearest obstacle distances
    
    node.publish_state(dummy_position, dummy_obstacles)
    
    # Keep alive for demonstration
    import time
    time.sleep(2)
    node.disconnect()

MQTT_BROKER = "192.168.1.100"
client = mqtt.Client("neurobot01")
client.connect(MQTT_BROKER)

def publish_state(position, obstacles):
    msg = f"{position[0]},{position[1]},{position[2]};{obstacles}"
    client.publish("neurobot/swarm", msg)
