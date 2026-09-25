"""Deterministic mock sensors for development and tests."""
from .camera import CameraFrame
from .lidar import LidarSample

def mock_lidar(count: int = 8, distance_m: float = 2.0) -> LidarSample:
    return LidarSample(ranges=[distance_m] * count)

def mock_camera(payload: object = None) -> CameraFrame:
    return CameraFrame(data=payload)
