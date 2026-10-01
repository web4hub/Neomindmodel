from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import numpy as np
import torch

@dataclass
class EDQState:
    vector: np.ndarray
    representation: np.ndarray
    path_clear: bool
    front_distance: float
    confidence: float

class EDQProcessor:
    """Adapter from heterogeneous robot sensors to the existing 16-D EDQ interface."""
    def __init__(self, model: Any | None = None, device: str | None = None):
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        self.model = model
        if model is not None:
            model.to(self.device).eval()

    @staticmethod
    def _lidar_features(lidar: Any) -> np.ndarray:
        v=np.asarray(lidar,dtype=np.float32).reshape(-1)
        if v.size==0: return np.ones(8,dtype=np.float32)*10
        return np.asarray([float(np.min(x)) for x in np.array_split(v,8)],dtype=np.float32)

    @staticmethod
    def _camera_features(camera: Any) -> np.ndarray:
        if camera is None: return np.zeros(6,dtype=np.float32)
        a=np.asarray(camera)
        if a.size==0: return np.zeros(6,dtype=np.float32)
        a=a.astype(np.float32)
        p10,p50,p90=np.percentile(a,[10,50,90]); edge=float(np.mean(np.abs(np.diff(a,axis=-1)))) if a.shape[-1]>1 else 0
        return np.asarray([a.mean(),a.std(),p10,p50,p90,edge],dtype=np.float32)/255.0

    def vectorize(self, data: dict[str,Any]) -> np.ndarray:
        lidar=self._lidar_features(data.get("lidar",[])); cam=self._camera_features(data.get("camera"))
        distance=np.asarray([float(data.get("front_distance",lidar[0]))],dtype=np.float32)
        imu=np.asarray([float(data.get("imu_angle",0.0))],dtype=np.float32)
        return np.concatenate([lidar,cam,distance,imu]).astype(np.float32)[:16]

    def process(self,data:dict[str,Any])->EDQState:
        vector=self.vectorize(data); front=float(data.get("front_distance",vector[0]))
        rep=vector.copy()
        if self.model is not None and hasattr(self.model,"edq"):
            with torch.no_grad(): rep=self.model.edq(torch.from_numpy(vector).unsqueeze(0).to(self.device)).squeeze(0).cpu().numpy()
        return EDQState(vector,rep,front>1.0,front,float(np.clip(front/3.0,0,1)))
