"""Dependency-free NeoMind host/device protocol."""

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
    if not command or "\n" in command or "\r" in command:
        raise ValueError("command must be a non-empty single-line string")
    return (
        json.dumps({"id": message_id, "cmd": command, **payload}, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def decode_message(line: str | bytes) -> dict[str, Any]:
    if isinstance(line, bytes):
        line = line.decode("utf-8")
    try:
        value = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid protocol JSON") from exc
    if not isinstance(value, dict):
        raise ValueError("protocol message must be a JSON object")
    return value


def make_message(message_id: str | int, command: str, **payload: Any) -> Message:
    return Message(message_id=message_id, command=command, payload=payload)
