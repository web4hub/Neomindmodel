"""Dependency-free NeoMind serial protocol helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Message:
    message_id: str | int
    command: str
    payload: dict[str, Any]


def encode_command(message_id: str | int, command: str, **payload: Any) -> bytes:
    if not command or "\n" in command:
        raise ValueError("command must be a non-empty single-line string")
    message = {"id": message_id, "cmd": command, **payload}
    return (json.dumps(message, separators=(",", ":")) + "\n").encode("utf-8")


def decode_message(line: str | bytes) -> dict[str, Any]:
    if isinstance(line, bytes):
        line = line.decode("utf-8")
    value = json.loads(line)
    if not isinstance(value, dict):
        raise ValueError("protocol message must be a JSON object")
    return value


def make_message(message_id: str | int, command: str, **payload: Any) -> Message:
    return Message(message_id=message_id, command=command, payload=payload)
