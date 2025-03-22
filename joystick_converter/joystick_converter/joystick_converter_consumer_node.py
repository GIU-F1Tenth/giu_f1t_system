import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import socket
import pickle


class JoyNetworkConsumer(Node):
    def __init__(self):
        super().__init__('joy_network_consumer')

        # Declare and get parameters
        self.declare_parameter('listen_ip', '0.0.0.0')
        self.declare_parameter('listen_port', 5000)

        self.listen_ip = self.get_parameter(
            'listen_ip').get_parameter_value().string_value
        self.listen_port = self.get_parameter(
            'listen_port').get_parameter_value().integer_value

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.listen_ip, self.listen_port))

        # Publisher to /joy topic
        self.publisher = self.create_publisher(Joy, '/joy', 10)

        self.get_logger().info(
            f"Listening for /joy messages on {self.listen_ip}:{self.listen_port}")

        # Timer to poll for incoming messages
        self.timer = self.create_timer(0.01, self.receive_data)

    def receive_data(self):
        try:
            # Receive data from the network
            data, _ = self.sock.recvfrom(65535)

            # Deserialize the Joy message
            msg = pickle.loads(data)

            # Publish the message to the /joy topic
            self.publisher.publish(msg)
        except Exception as e:
            self.get_logger().error(
                f"Failed to receive or publish /joy message: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = JoyNetworkConsumer()

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
