import unittest
import numpy as np
from robotics.sensors.lidar_reader import LIDAR_SIZE,SENSOR_VECTOR_SIZE,get_sensor_vector
from robotics.sensors.reflex import AdvancedSensorReflex,ReflexController

class SensorVectorTests(unittest.TestCase):
    def test_default_vector_shape(self):
        v=get_sensor_vector(); self.assertEqual(v.shape,(SENSOR_VECTOR_SIZE,)); self.assertEqual(v.dtype,np.float32)
    def test_imu_vector_shape(self):
        self.assertEqual(get_sensor_vector(include_imu=True).shape,(SENSOR_VECTOR_SIZE+1,))

class ReflexTests(unittest.TestCase):
    def test_controller_output_contract(self):
        c=ReflexController(AdvancedSensorReflex())
        out=c.predict(np.zeros(SENSOR_VECTOR_SIZE,dtype=np.float32))
        self.assertTrue(all(0.0<=x<=1.0 for x in (out.throttle,out.steering,out.capture_trigger,out.aux)))
    def test_wrong_shape_rejected(self):
        c=ReflexController(AdvancedSensorReflex())
        with self.assertRaises(ValueError): c.predict(np.zeros(12,dtype=np.float32))

if __name__=="__main__": unittest.main()
