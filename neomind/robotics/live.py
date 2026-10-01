from __future__ import annotations
from typing import Any
try:
    from sensors.lidar_reader import read_distance, read_lidar, read_imu
except ImportError:
    read_distance=read_lidar=read_imu=None
try:
    from sensors.Camera import MockSensors
except ImportError:
    MockSensors=None

class RepositorySensorAdapter:
    """Bridge the existing repository sensor modules into NeoMind's sensor contract."""
    def __init__(self, camera: Any|None=None): self.camera=camera or (MockSensors() if MockSensors else None)
    def read(self):
        lidar=read_lidar() if read_lidar else []
        distance=read_distance() if read_distance else (min(lidar) if lidar else 10.0)
        imu=read_imu() if read_imu else 0.0
        camera=self.camera.read_camera() if self.camera and hasattr(self.camera,"read_camera") else None
        return {"lidar":lidar,"front_distance":float(distance),"imu_angle":float(imu),"camera":camera}
