"""Host-side neural sensor-reflex inference."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import torch
import torch.nn as nn
from .lidar_reader import get_sensor_vector

@dataclass(frozen=True)
class ReflexCommand:
    throttle: float
    steering: float
    capture_trigger: float
    aux: float

class AdvancedSensorReflex(nn.Module):
    def __init__(self,input_dim:int=361,hidden_dim:int=256,output_dim:int=4):
        super().__init__()
        self.feature_extractor=nn.Sequential(nn.Linear(input_dim,hidden_dim),nn.LayerNorm(hidden_dim),nn.GELU(),nn.Linear(hidden_dim,hidden_dim),nn.LayerNorm(hidden_dim),nn.GELU())
        self.control_head=nn.Sequential(nn.Linear(hidden_dim,64),nn.GELU(),nn.Linear(64,output_dim),nn.Sigmoid())
    def forward(self,x:torch.Tensor)->torch.Tensor:
        return self.control_head(self.feature_extractor(x))

class ReflexController:
    def __init__(self,model:AdvancedSensorReflex):
        self.model=model.eval()
    @torch.inference_mode()
    def predict(self,sensor_vector:np.ndarray)->ReflexCommand:
        if sensor_vector.ndim!=1: raise ValueError("sensor_vector must be one-dimensional")
        expected=self.model.feature_extractor[0].in_features
        if sensor_vector.shape[0]!=expected: raise ValueError(f"expected {expected} sensor values, got {sensor_vector.shape[0]}")
        output=self.model(torch.as_tensor(sensor_vector,dtype=torch.float32).unsqueeze(0)).squeeze(0).cpu().numpy()
        return ReflexCommand(*map(float,output))

def run_simulation(cycles:int=3,hz:float=20.0)->list[ReflexCommand]:
    if cycles<1: raise ValueError("cycles must be >= 1")
    if hz<=0: raise ValueError("hz must be > 0")
    import time
    controller=ReflexController(AdvancedSensorReflex())
    results=[]
    for _ in range(cycles):
        results.append(controller.predict(get_sensor_vector()))
        time.sleep(1.0/hz)
    return results

if __name__=="__main__":
    for i,c in enumerate(run_simulation(),1):
        print(f"[Cycle {i}] throttle={c.throttle:.2f} steering={c.steering:.2f} capture={c.capture_trigger:.2f} aux={c.aux:.2f}")
