import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import socket
import pickle


class JoyNetworkPublisher(Node):
    def __init__(self):
        super().__init__('joy_network_publisher')

        # Declare and get parameters
        self.declare_parameter('target_ip', '127.0.0.1')
        self.declare_parameter('target_port', 5000)

        self.target_ip = self.get_parameter(
            'target_ip').get_parameter_value().string_value
        self.target_port = self.get_parameter(
            'target_port').get_parameter_value().integer_value

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Subscriber to /joy topic
        self.subscription = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            10
        )

        self.get_logger().info(
            f"Publishing /joy messages to {self.target_ip}:{self.target_port}")

    def joy_callback(self, msg):
        try:
            # Serialize the Joy message
            serialized_msg = pickle.dumps(msg)

            # Send the serialized message over the network
            self.sock.sendto(
                serialized_msg, (self.target_ip, self.target_port))

            self.get_logger().info("Sent /joy message over the network")
        except Exception as e:
            self.get_logger().error(f"Failed to send /joy message: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = JoyNetworkPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.sock.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
