"""Inventory of legacy subsystems and their v2 migration boundaries."""

from dataclasses import dataclass

@dataclass(frozen=True)
class MigrationTarget:
    legacy_area: str
    v2_boundary: str
    status: str

MIGRATION_TARGETS = (
    MigrationTarget("Brain/neomind", "neomind.device + neomind.runtime", "adapter-ready"),
    MigrationTarget("Brain/robotics", "neomind.device", "adapter-ready"),
    MigrationTarget("sensor + sensors", "host sensor adapters", "preserve-and-migrate"),
    MigrationTarget("pythonAi", "host AI provider adapter", "preserve-and-migrate"),
    MigrationTarget("ros2", "ROS 2 bridge", "preserve-and-migrate"),
    MigrationTarget("serial", "NeoMind protocol transport", "adapter-ready"),
)

def inventory() -> tuple[MigrationTarget, ...]: return MIGRATION_TARGETS
