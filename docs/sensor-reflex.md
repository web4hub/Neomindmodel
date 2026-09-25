# Sensor → Reflex pipeline

LiDAR (360) + distance → float32 sensor vector → host-side PyTorch reflex model → named ReflexCommand.

The default vector contains 361 values; optional IMU support produces 362. Sensor acquisition is isolated from inference so hardware adapters can replace simulation providers without coupling them to the model.

The included model is an untrained architecture for simulation/testing. It is not a trained autonomous policy. The simulation loop performs inference only and does not write to real actuators.

Production hardware integration should separately validate calibration, normalization, model checkpoints, safety limits, watchdogs, and actuator interlocks.
