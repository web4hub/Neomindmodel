from neomind.robotics.robot import Robot
from neomind.brain.edq import EDQProcessor
from neomind.brain.serai import SERAILayer

class MockDistanceSensor:
    def __init__(self,d=3.0): self.d=d
    def read(self): return self.d
class MockCamera:
    def read(self): return [[0]*32 for _ in range(24)]
class MockMotor:
    def __init__(self): self.speed=0
    def set_speed(self,s): self.speed=s
    def stop(self): self.speed=0
class MockLED:
    def on(self): pass
    def off(self): pass
    def blink(self): pass

if __name__ == "__main__":
    r=Robot("neurobot-01",MockDistanceSensor(),MockCamera(),MockMotor(),MockMotor(),MockLED(),EDQProcessor(),SERAILayer())
    for _ in range(10): print(r.step())
    r.stop()
