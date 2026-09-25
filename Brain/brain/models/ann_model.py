"""Minimal artificial-neural-network interface."""
class ANNModel:
    def predict(self, features: list[float]) -> list[float]:
        return [float(x) for x in features]
