"""NeoMind sensor package.

Sensor acquisition is lightweight; neural reflex components are optional and
imported lazily so sensor-only deployments do not require PyTorch.
"""

from .lidar_reader import get_sensor_vector, read_distance, read_imu, read_lidar

__all__ = [
    "get_sensor_vector",
    "read_distance",
    "read_imu",
    "read_lidar",
]


def __getattr__(name: str):
    if name in {"AdvancedSensorReflex", "ReflexCommand", "ReflexController"}:
        from .reflex import AdvancedSensorReflex, ReflexCommand, ReflexController

        return {
            "AdvancedSensorReflex": AdvancedSensorReflex,
            "ReflexCommand": ReflexCommand,
            "ReflexController": ReflexController,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
