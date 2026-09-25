from brain.sensors.mock_sensors import mock_lidar

def test_mock_lidar():
    sample = mock_lidar(4, 3.0)
    assert len(sample.ranges) == 4
    assert sample.ranges[0] == 3.0
