"""Hardware-neutral motor controller interface."""
class MotorController:
    def __init__(self) -> None:
        self.left = 0.0
        self.right = 0.0
    def set_velocity(self, left: float, right: float) -> tuple[float, float]:
        self.left, self.right = float(left), float(right)
        return self.left, self.right
    def stop(self) -> None:
        self.set_velocity(0.0, 0.0)
