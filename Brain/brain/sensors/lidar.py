"""LiDAR sensor abstraction for NeoMind Brain."""
from dataclasses import dataclass
from typing import Iterable

@dataclass
class LidarSample:
    ranges: list[float]
    timestamp: float | None = None

class LidarSensor:
    def __init__(self, max_range_m: float = 30.0) -> None:
        self.max_range_m = max_range_m
    def read(self, ranges: Iterable[float]) -> LidarSample:
        values = [min(max(float(r), 0.0), self.max_range_m) for r in ranges]
        return LidarSample(ranges=values)
