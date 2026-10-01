from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any,Protocol
@dataclass
class Decision:
    move_forward: bool=False; turn: bool=False; turn_angle: float=0.0
    left_speed: float=0.0; right_speed: float=0.0; stop: bool=True
    path_clear: bool=False; confidence: float=0.0; metadata: dict[str,Any]=field(default_factory=dict)
class SERAIBackend(Protocol):
    def decide(self,state:Any)->Decision: ...
class SERAILayer:
    """Policy boundary for trained SERAI; deterministic fallback keeps robotics runnable now."""
    def __init__(self,backend:SERAIBackend|None=None): self.backend=backend
    def decide(self,state:Any)->Decision:
        if self.backend: return self.backend.decide(state)
        d=float(state.front_distance)
        if d<=0.5: return Decision(turn=True,turn_angle=90,stop=False,confidence=1,metadata={"reason":"immediate_obstacle"})
        if d<=1.5: return Decision(turn=True,turn_angle=45,left_speed=-.25,right_speed=.25,stop=False,confidence=.85,metadata={"reason":"obstacle_avoidance"})
        return Decision(move_forward=True,left_speed=.6,right_speed=.6,stop=False,path_clear=True,confidence=.9,metadata={"reason":"clear_path"})
