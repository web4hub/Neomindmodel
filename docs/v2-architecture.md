# NeoMind v2 Architecture

## Layers

```
+-----------------------------+
| Host AI / Web4 / ROS2       |
+-------------+---------------+
              |
        NeoMind protocol
              |
+-------------v---------------+
| USB serial / 115200 baud    |
+-------------+---------------+
              |
+-------------v---------------+
| ATmega328P firmware         |
| deterministic I/O + status  |
+-----------------------------+
```

The board owns timing-sensitive I/O and a small command surface. Host software owns model inference, networking, persistence, orchestration, and resource-heavy processing.

## Hardware assumptions

The repository identifies the target as Neomind Board v1 with an ATmega328P-compatible Arduino target and USB-B support for power, serial communication, and firmware upload. Pin assignments beyond those explicitly documented in the repository must be treated as board-specific configuration rather than guessed.

## Protocol design

Messages are newline-delimited JSON. Every request should carry an integer/string `id`. The firmware implements a small allow-list of commands and returns an explicit `ok` flag.

This keeps the wire contract stable while host implementations evolve.

## Upgrade path

1. Stabilize serial protocol.
2. Add board-specific pin map once the schematic is authoritative.
3. Add host serial transport.
4. Add optional AI/Web4 adapters on the host.
5. Add signed firmware manifests and integrity checks.
6. Add a network bridge if OTA is required.

OTA is not assumed to be native to the ATmega328P board; a network-capable bridge is required.
