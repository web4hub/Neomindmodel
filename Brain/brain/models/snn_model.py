"""Minimal spiking-neural-network interface."""
class SNNModel:
    def __init__(self, threshold: float = 1.0) -> None:
        self.threshold = threshold
    def spike(self, value: float) -> int:
        return int(float(value) >= self.threshold)
