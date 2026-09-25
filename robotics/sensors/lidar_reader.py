"""Sensor acquisition and vector construction for NeoMind."""
from __future__ import annotations
import numpy as np

LIDAR_SIZE = 360
SENSOR_VECTOR_SIZE = LIDAR_SIZE + 1

def read_lidar() -> list[float]:
    return np.random.rand(LIDAR_SIZE).astype(np.float32).tolist()

def read_distance() -> float:
    return float(np.random.rand())

def read_imu() -> float:
    return float(np.random.rand())

def get_sensor_vector(*, include_imu: bool = False) -> np.ndarray:
    lidar = read_lidar()
    if len(lidar) != LIDAR_SIZE:
        raise ValueError(f"LiDAR scan must contain {LIDAR_SIZE} samples")
    values = lidar + [read_distance()]
    if include_imu:
        values.append(read_imu())
    return np.asarray(values, dtype=np.float32)
