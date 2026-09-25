import rclpy
from rclpy.node import Node

class ImuNode(Node):
    def __init__(self):
        super().__init__("neomind_imu")
        self.get_logger().info("NeoMind IMU node ready")

def main(args=None):
    rclpy.init(args=args)
    node = ImuNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
