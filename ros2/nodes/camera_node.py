import rclpy
from rclpy.node import Node

class CameraNode(Node):
    def __init__(self):
        super().__init__("neomind_camera")
        self.get_logger().info("NeoMind camera node ready")

def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
