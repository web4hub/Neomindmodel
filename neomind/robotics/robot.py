from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import time
from neomind.brain.edq import EDQProcessor
from neomind.brain.serai import SERAILayer,Decision
@dataclass
class Robot:
    robot_id:str; front:Any; vision:Any; left_wheel:Any; right_wheel:Any; status_led:Any; edq:EDQProcessor; serai:SERAILayer; communication:Any|None=None; learner:Any|None=None; running:bool=True
    def read_sensors(self):
        d=float(self.front.read()); return {"robot_id":self.robot_id,"front_distance":d,"lidar":[d]*360,"camera":self.vision.read(),"timestamp":time.time()}
    def execute_decision(self,x:Decision):
        if x.stop: self.left_wheel.stop(); self.right_wheel.stop()
        elif x.move_forward: self.left_wheel.set_speed(x.left_speed); self.right_wheel.set_speed(x.right_speed)
        elif x.turn:
            s=.4 if x.turn_angle>=0 else -.4; self.left_wheel.set_speed(-s); self.right_wheel.set_speed(s)
    def step(self):
        data=self.read_sensors(); state=self.edq.process(data); decision=self.serai.decide(state); self.execute_decision(decision)
        if self.communication: self.communication.broadcast({"robot_id":self.robot_id,"sensor_data":data,"decision":decision.__dict__}); self.communication.sync_nearby(self.robot_id)
        if self.learner: self.learner.observe(data,state,decision)
        (self.status_led.on if decision.path_clear else self.status_led.blink)(); return decision
    def stop(self): self.running=False; self.left_wheel.stop(); self.right_wheel.stop(); self.status_led.off()
    def run(self,interval=.05):
        try:
            while self.running: self.step(); time.sleep(interval)
        finally: self.stop()
