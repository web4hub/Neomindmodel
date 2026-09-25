"""Camera sensor abstraction for NeoMind Brain."""
from dataclasses import dataclass
from typing import Any

@dataclass
class CameraFrame:
    data: Any
    timestamp: float | None = None

class CameraSensor:
    def capture(self, frame: Any) -> CameraFrame:
        return CameraFrame(data=frame)
