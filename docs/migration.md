# NeoMind legacy migration

NeoMind v2 is an incremental migration, not a destructive rewrite.

## Boundaries

- Firmware: deterministic ATmega328P control and serial protocol.
- Runtime: host-side transport, device API, and orchestration.
- Sensors: camera, LiDAR, radar, and other sensor adapters remain host-side.
- AI: model inference remains host-side.
- Robotics: motor and motion logic is exposed through host adapters before device commands.
- ROS 2, MQTT, and Web4 integrations remain outside MCU firmware.

Legacy directories are retained until each subsystem has a tested v2 replacement or adapter.

| Legacy area | v2 boundary | State |
|---|---|---|
| Brain/neomind | neomind.device / neomind.runtime | adapter-ready |
| Brain/robotics | neomind.device | adapter-ready |
| sensor, sensors | host sensor adapters | preserve-and-migrate |
| pythonAi | host AI provider adapter | preserve-and-migrate |
| ros2 | ROS 2 bridge | preserve-and-migrate |
| serial | protocol transport | adapter-ready |

No legacy subsystem is deleted by this migration layer.
