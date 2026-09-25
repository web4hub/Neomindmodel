import rclpy
from rclpy.node import Node

class SwarmNode(Node):
    def __init__(self):
        super().__init__("neomind_swarm")
        self.get_logger().info("NeoMind swarm node ready")

def main(args=None):
    rclpy.init(args=args)
    node = SwarmNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
