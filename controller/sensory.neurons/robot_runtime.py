# robot_runtime.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol
import time


# ============================================================
# Sensor / actuator interfaces
# ============================================================

class DistanceSensor(Protocol):
    def read(self) -> float: ...


class Camera(Protocol):
    def read(self) -> Any: ...


class Motor(Protocol):
    def set_speed(self, speed: float) -> None: ...
    def stop(self) -> None: ...


class LED(Protocol):
    def on(self) -> None: ...
    def off(self) -> None: ...
    def blink(self) -> None: ...


# ============================================================
# AI decision model
# ============================================================

@dataclass
class Decision:
    move_forward: bool = False
    turn: bool = False
    turn_angle: float = 0.0

    left_speed: float = 0.0
    right_speed: float = 0.0

    stop: bool = True
    path_clear: bool = False

    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class EDQLayer:
    """
    Exploration / Detection / Query representation layer.

    Converts heterogeneous robot observations into a normalized
    representation consumed by SERAI.
    """

    def process(self, sensor_data: dict[str, Any]) -> dict[str, Any]:
        distance = float(sensor_data.get("front_distance", 999.0))

        return {
            "front_distance": distance,
            "vision": sensor_data.get("vision"),
            "path_clear": distance > 1.0,
            "obstacle_level": max(0.0, 1.0 - min(distance / 5.0, 1.0)),
            "timestamp": sensor_data.get("timestamp"),
        }


class SERAILayer:
    """
    Decision/action layer.

    In the full NeoMind system this becomes the learned SERAI
    policy/model rather than the rule-based fallback below.
    """

    def decide(self, processed: dict[str, Any]) -> Decision:
        distance = processed["front_distance"]

        if distance <= 0.5:
            return Decision(
                stop=True,
                turn=True,
                turn_angle=90.0,
                path_clear=False,
                confidence=1.0,
                metadata={"reason": "immediate_obstacle"},
            )

        if distance <= 1.5:
            return Decision(
                turn=True,
                turn_angle=45.0,
                left_speed=-0.25,
                right_speed=0.25,
                path_clear=False,
                confidence=0.85,
                metadata={"reason": "obstacle_avoidance"},
            )

        return Decision(
            move_forward=True,
            left_speed=0.6,
            right_speed=0.6,
            stop=False,
            path_clear=True,
            confidence=0.9,
            metadata={"reason": "clear_path"},
        )


# ============================================================
# Robot
# ============================================================

@dataclass
class Robot:
    robot_id: str

    front: DistanceSensor
    vision: Camera

    left_wheel: Motor
    right_wheel: Motor

    status_led: LED

    edq: EDQLayer
    serai: SERAILayer

    communication: Any | None = None
    learner: Any | None = None

    running: bool = True

    # --------------------------------------------------------
    # Sensor acquisition
    # --------------------------------------------------------

    def read_sensors(self) -> dict[str, Any]:
        return {
            "robot_id": self.robot_id,
            "front_distance": self.front.read(),
            "vision": self.vision.read(),
            "timestamp": time.time(),
        }

    # --------------------------------------------------------
    # Actuation
    # --------------------------------------------------------

    def stop_motors(self) -> None:
        self.left_wheel.stop()
        self.right_wheel.stop()

    def execute_decision(self, decision: Decision) -> None:
        if decision.stop:
            self.stop_motors()

        elif decision.move_forward:
            self.left_wheel.set_speed(decision.left_speed)
            self.right_wheel.set_speed(decision.right_speed)

        elif decision.turn:
            # Differential-drive turning.
            speed = 0.4 if decision.turn_angle >= 0 else -0.4

            self.left_wheel.set_speed(-speed)
            self.right_wheel.set_speed(speed)

    # --------------------------------------------------------
    # Swarm communication
    # --------------------------------------------------------

    def broadcast(self, sensor_data: dict[str, Any], decision: Decision) -> None:
        if self.communication is None:
            return

        self.communication.broadcast(
            {
                "robot_id": self.robot_id,
                "sensor_data": sensor_data,
                "decision": decision.__dict__,
            }
        )

    def synchronize(self) -> None:
        if self.communication is not None:
            self.communication.sync_nearby(self.robot_id)

    # --------------------------------------------------------
    # Learning
    # --------------------------------------------------------

    def train_on_feedback(
        self,
        sensor_data: dict[str, Any],
        processed: dict[str, Any],
        decision: Decision,
    ) -> None:
        if self.learner is None:
            return

        self.learner.observe(
            {
                "sensor_data": sensor_data,
                "processed": processed,
                "decision": decision.__dict__,
            }
        )

    # --------------------------------------------------------
    # Status LED
    # --------------------------------------------------------

    def update_status(self, decision: Decision) -> None:
        if decision.path_clear:
            self.status_led.on()
        else:
            self.status_led.blink()

    # --------------------------------------------------------
    # Main NeoMind loop
    # --------------------------------------------------------

    def step(self) -> Decision:
        # 1. Perception
        sensor_data = self.read_sensors()

        # 2. EDQ representation / processing
        processed = self.edq.process(sensor_data)

        # 3. SERAI decision
        decision = self.serai.decide(processed)

        # 4. Act
        self.execute_decision(decision)

        # 5. Swarm communication
        self.broadcast(sensor_data, decision)
        self.synchronize()

        # 6. Continuous learning
        self.train_on_feedback(
            sensor_data,
            processed,
            decision,
        )

        # 7. Status
        self.update_status(decision)

        return decision

    def run(self, interval: float = 0.05) -> None:
        try:
            while self.running:
                decision = self.step()

                print(
                    f"[Robot {self.robot_id}] "
                    f"decision={decision.metadata.get('reason')} "
                    f"confidence={decision.confidence:.2f}"
                )

                time.sleep(interval)

        finally:
            self.stop_motors()
            self.status_led.off()

    def shutdown(self) -> None:
        self.running = False
        self.stop_motors()
        self.status_led.off()
