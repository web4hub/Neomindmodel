import serial
import time

class ArduinoActuatorBridge:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Allow Arduino to reset
            print(f"[Actuators] Connected to Arduino on {port}")
        except Exception as e:
            print(f"[Actuators Error] Could not connect to serial port: {e}")
            self.ser = None

    def send_command(self, action: str):
        if self.ser and self.ser.is_open:
            command_string = f"{action}\n"
            self.ser.write(command_string.encode('utf-8'))

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
