"""Boundary for legacy AI, ROS 2, MQTT, camera, and sensor integrations."""

from __future__ import annotations
from typing import Any
from .device import NeoMindDevice

class NeoMindBridge:
    def __init__(self, device: NeoMindDevice): self.device = device
    def health(self) -> dict[str, Any]: return self.device.status(message_id="health")
    def command(self, command: str, **payload: Any) -> dict[str, Any]:
        if command == "ping": return self.device.ping(message_id="bridge")
        if command == "status": return self.device.status(message_id="bridge")
        if command == "set_led": return self.device.set_led(bool(payload.get("value")), message_id="bridge")
        raise ValueError(f"unsupported bridge command: {command}")
