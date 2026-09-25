import unittest

import numpy as np

from robotics.sensors.lidar_reader import LIDAR_SIZE, SENSOR_VECTOR_SIZE, get_sensor_vector

try:
    from robotics.sensors.reflex import AdvancedSensorReflex, ReflexController
    TORCH_AVAILABLE = True
except ModuleNotFoundError as exc:
    if exc.name != "torch":
        raise
    TORCH_AVAILABLE = False


class SensorVectorTests(unittest.TestCase):
    def test_default_vector_shape(self):
        vector = get_sensor_vector()
        self.assertEqual(vector.shape, (SENSOR_VECTOR_SIZE,))
        self.assertEqual(vector.dtype, np.float32)

    def test_imu_vector_shape(self):
        vector = get_sensor_vector(include_imu=True)
        self.assertEqual(vector.shape, (SENSOR_VECTOR_SIZE + 1,))

    def test_lidar_size_contract(self):
        self.assertEqual(LIDAR_SIZE, 360)


@unittest.skipUnless(TORCH_AVAILABLE, "PyTorch is not installed")
class ReflexTests(unittest.TestCase):
    def test_controller_output_contract(self):
        controller = ReflexController(AdvancedSensorReflex())
        output = controller.predict(
            np.zeros(SENSOR_VECTOR_SIZE, dtype=np.float32)
        )
        self.assertTrue(
            all(
                0.0 <= value <= 1.0
                for value in (
                    output.throttle,
                    output.steering,
                    output.capture_trigger,
                    output.aux,
                )
            )
        )

    def test_wrong_shape_rejected(self):
        controller = ReflexController(AdvancedSensorReflex())
        with self.assertRaises(ValueError):
            controller.predict(np.zeros(12, dtype=np.float32))


if __name__ == "__main__":
    unittest.main()
