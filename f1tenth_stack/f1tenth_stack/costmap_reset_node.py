import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty

class CostmapResetNode(Node):
    def __init__(self):
        super().__init__('costmap_reset_node')

        # Create service clients
        # self.local_client = self.create_client(Empty, '/local_costmap/clear_entirely_local_costmap')
        self.global_client = self.create_client(Empty, '/global_costmap/clear_entirely_global_costmap')

        # Wait for services to be available
        self.get_logger().info('Waiting for costmap clear services...')
        # self.local_client.wait_for_service()
        self.global_client.wait_for_service()
        self.get_logger().info('Costmap clear services available.')

        # Set up a timer to call every 3 seconds
        self.timer = self.create_timer(3.0, self.reset_costmaps)

    def reset_costmaps(self):
        # self.get_logger().info('Resetting local and global costmaps...')
        req = Empty.Request()
        # self.local_client.call_async(req)
        self.global_client.call_async(req)

def main(args=None):
    rclpy.init(args=args)
    node = CostmapResetNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
