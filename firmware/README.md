# NeoMind firmware

This directory is the authoritative PlatformIO project for the NeoMind Board v1-compatible ATmega328P target.

Build from the repository root:

```bash
pio run -d firmware -e neomind_v1
```

The board exposes newline-delimited JSON over USB serial at 115200 baud. Heavy AI, Web4, networking, and persistence belong on the host runtime.
