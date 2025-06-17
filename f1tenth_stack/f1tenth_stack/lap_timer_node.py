import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math
import time


class LapTimerNode(Node):
    def __init__(self):
        super().__init__('lap_timer_node')
        self.get_logger().info('Lap Timer Node Initialized')

        self.sub_odom = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)

        # States
        # Has the vehicle started moving from the initial position?
        self.has_started = False
        self.start_time = None
        self.start_position = None
        self.lap_count = 0
        self.lap_times = []

        # Parameters
        # Minimum speed to consider the vehicle has started moving
        self.speed_threshold = 0.01
        # Distance threshold to consider returning to start line
        self.return_threshold = 0.5
        # Distance threshold to consider that the vehicle left start area
        self.away_threshold = 2.0

        self.vehicle_away = False      # Did the vehicle leave the start area after start?

    def odom_callback(self, msg: Odometry):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        vx = msg.twist.twist.linear.x
        vy = msg.twist.twist.linear.y

        speed = math.sqrt(vx*vx + vy*vy)

        # If not started, check if speed is above threshold to start timing
        if not self.has_started:
            if speed > self.speed_threshold:
                # Initialize start
                self.has_started = True
                self.start_time = time.time()
                self.start_position = (x, y)
                self.vehicle_away = False
                self.get_logger().info("Vehicle started moving. Starting lap timing...")
            return

        # If we have started, we're tracking laps
        dist_from_start = self.distance((x, y), self.start_position)

        # Check if the vehicle has gone away from start line
        if not self.vehicle_away and dist_from_start > self.away_threshold:
            self.vehicle_away = True

        # If we have moved away and come back within threshold, it means a lap is completed
        if self.vehicle_away and dist_from_start < self.return_threshold:
            # Complete a lap
            lap_time = time.time() - self.start_time
            self.lap_times.append(lap_time)
            self.lap_count += 1
            self.get_logger().info(
                f"Lap {self.lap_count} completed in {lap_time:.2f} seconds.")

            # Reset for next lap
            self.start_time = time.time()
            self.vehicle_away = False

            # If 5 laps completed, print stats
            if self.lap_count == 5:
                self.print_stats()
                # You could shut down after printing if desired
                # rclpy.shutdown()

    def distance(self, p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def print_stats(self):
        average_time = sum(self.lap_times) / len(self.lap_times)
        best_time = min(self.lap_times)
        worst_time = max(self.lap_times)

        self.get_logger().info("\n------ Lap Times ------")
        for i, t in enumerate(self.lap_times, start=1):
            self.get_logger().info(f"Lap {i}: {t:.2f}s")

        self.get_logger().info("-----------------------")
        self.get_logger().info(f"Average time: {average_time:.2f}s")
        self.get_logger().info(f"Best time:    {best_time:.2f}s")
        self.get_logger().info(f"Worst time:   {worst_time:.2f}s")
        self.get_logger().info("-----------------------")


def main(args=None):
    rclpy.init(args=args)
    node = LapTimerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
