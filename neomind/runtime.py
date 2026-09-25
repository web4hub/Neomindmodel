"""Small host runtime facade.

Heavy AI, networking, and robotics dependencies stay outside this core module.
"""

from __future__ import annotations

from typing import Protocol


class Transport(Protocol):
    def write(self, data: bytes) -> None: ...
    def readline(self) -> bytes: ...


class NeoMindRuntime:
    def __init__(self, transport: Transport):
        self.transport = transport

    def request(self, message_id: str | int, command: str, **payload):
        from .protocol import encode_command, decode_message

        self.transport.write(encode_command(message_id, command, **payload))
        return decode_message(self.transport.readline())
