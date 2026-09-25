from brain.sensors.mock_sensors import mock_lidar
from brain.models.snn_model import SNNModel

def main() -> None:
    sample = mock_lidar()
    model = SNNModel()
    print({"ranges": sample.ranges, "spikes": [model.spike(r) for r in sample.ranges]})

if __name__ == "__main__":
    main()
