# NeoMind Robot Runtime

Sensors -> EDQ -> SERAI -> actuators -> swarm synchronization -> feedback.

The runtime adds a stable robotics boundary around the existing EDQ code. EDQ normalizes LiDAR/camera/IMU observations into the existing 16-feature interface and can optionally use a learned EDQ projection. SERAI is a policy boundary with a deterministic obstacle-avoidance fallback until a trained SERAI decoder/policy is wired in.

The runtime is intentionally hardware-agnostic so the same control loop can run in simulation before real robot drivers are attached.
