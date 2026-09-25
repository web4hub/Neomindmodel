"""Device abstraction over the NeoMind serial protocol."""

from __future__ import annotations
from typing import Any
from .runtime import NeoMindRuntime

class NeoMindDevice:
    """High-level, hardware-independent device API."""
    def __init__(self, runtime: NeoMindRuntime): self.runtime = runtime
    def ping(self, message_id: str | int = 1) -> dict[str, Any]: return self.runtime.request(message_id, "ping")
    def status(self, message_id: str | int = 2) -> dict[str, Any]: return self.runtime.request(message_id, "status")
    def set_led(self, value: bool, message_id: str | int = 3) -> dict[str, Any]: return self.runtime.request(message_id, "set_led", value=value)
