# NeoMind Model

NeoMind is a robotics/embedded AI workspace combining an ATmega328P-compatible controller, host-side intelligence, sensors, simulation, and Web4-facing integration points.

## v2 rebuild

The v2 layer is deliberately separated from the legacy tree so existing experiments remain recoverable while the core becomes testable and reproducible.

- `firmware/` — small deterministic firmware for the Neomind Board v1 / ATmega328P target.
- `neomind/` — host-side protocol and runtime primitives.
- `tests/` — dependency-light protocol tests.
- `.github/workflows/neomind-v2.yml` — CI for the v2 layer.
- `docs/v2-architecture.md` — architecture and hardware boundaries.

### Important hardware boundary

The ATmega328P is the device controller; it is not an appropriate target for running a full LLM. NeoMind therefore uses a serial protocol between the board and a host runtime. The host can later connect that runtime to an AI model, Web4 service, ROS 2, or other systems without changing the board protocol.

## Quick start

### Firmware

Install PlatformIO and run:

```bash
pio run -e neomind_v1
```

Upload with:

```bash
pio run -e neomind_v1 -t upload
```

The firmware exposes a newline-delimited JSON protocol over USB serial at 115200 baud.

### Host tests

```bash
python -m unittest discover -s tests -v
```

No third-party package is required for the protocol tests.

## Protocol

Commands use compact JSON objects:

```json
{"id":1,"cmd":"ping"}
{"id":2,"cmd":"status"}
{"id":3,"cmd":"set_led","value":1}
```

Responses contain the request id and a result:

```json
{"id":1,"ok":true,"result":{"pong":true}}
```

## Status

This branch is the reconstruction baseline. Existing legacy directories are intentionally not deleted until their functionality has been migrated and validated.
