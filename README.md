# NeoMind Model

NeoMind is a robotics/embedded AI workspace combining an ATmega328P-compatible controller, host-side intelligence, sensors, simulation, and Web4-facing integration points.

## v2 architecture

The rebuild is incremental:

- firmware/ — authoritative PlatformIO firmware project.
- neomind/ — host protocol, runtime, device API, bridge, and migration map.
- tests/ — dependency-light host tests.
- docs/v2-architecture.md — hardware/software boundary.
- docs/migration.md — legacy-to-v2 migration map.
- Legacy directories remain available until functionality is migrated and validated.

The ATmega328P is the device controller, not the LLM host. AI, Web4, ROS 2, MQTT, camera processing, and other heavyweight services belong on the host side.

## Quick start

Host tests:

    python -m unittest discover -s tests -v

Firmware build:

    pio run -d firmware -e neomind_v1

Firmware upload:

    pio run -d firmware -e neomind_v1 -t upload

Serial protocol: newline-delimited JSON at 115200 baud.

Example commands:

    {"id":1,"cmd":"ping"}
    {"id":2,"cmd":"status"}
    {"id":3,"cmd":"set_led","value":1}

Example response:

    {"id":1,"ok":true,"result":{"pong":true}}

## Migration

Use neomind.migration.inventory() to inspect migration boundaries. Existing Brain, sensor, AI, robotics, serial, and ROS 2 components are preserved while adapters are introduced.

See docs/migration.md for the current map.
