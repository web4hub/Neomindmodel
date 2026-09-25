"""Small host runtime facade for a serial-like transport."""

from __future__ import annotations

from typing import Protocol

from .protocol import decode_message, encode_command


class Transport(Protocol):
    def write(self, data: bytes) -> None: ...
    def readline(self) -> bytes: ...


class NeoMindRuntime:
    def __init__(self, transport: Transport):
        self.transport = transport

    def request(self, message_id: str | int, command: str, **payload):
        self.transport.write(encode_command(message_id, command, **payload))
        return decode_message(self.transport.readline())
