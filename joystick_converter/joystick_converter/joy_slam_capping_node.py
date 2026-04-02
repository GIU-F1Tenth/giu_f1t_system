#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from sensor_msgs.msg import Joy
from ackermann_msgs.msg import AckermannDriveStamped


class JoyAckermannFilter(Node):
    def __init__(self):
        super().__init__('joy_ackermann_filter')

        self.declare_parameter('joy_topic', '/joy_ackermann_filter')
        self.declare_parameter('cmd_topic', '/ackermann_cmd')
        self.declare_parameter('frame_id', 'base_link')

        self.declare_parameter('speed_axis', 1)
        self.declare_parameter('steering_axis', 2)

        self.declare_parameter('speed_sign', 1.0)
        self.declare_parameter('steering_sign', 1.0)

        self.declare_parameter('max_speed', 1.0)                # m/s
        self.declare_parameter('max_steering_angle', 0.34)      # rad

        self.declare_parameter('require_deadman', False)
        self.declare_parameter('deadman_button', 4)
        self.declare_parameter('publish_zero_on_release', True)

        self.declare_parameter('speed_scale', 1.0)
        self.declare_parameter('steering_scale', 1.0)

        self.joy_topic = self.get_parameter('joy_topic').value
        self.cmd_topic = self.get_parameter('cmd_topic').value
        self.frame_id = self.get_parameter('frame_id').value

        self.speed_axis = int(self.get_parameter('speed_axis').value)
        self.steering_axis = int(self.get_parameter('steering_axis').value)

        self.speed_sign = float(self.get_parameter('speed_sign').value)
        self.steering_sign = float(self.get_parameter('steering_sign').value)

        self.max_speed = float(self.get_parameter('max_speed').value)
        self.max_steering_angle = float(self.get_parameter('max_steering_angle').value)

        self.require_deadman = bool(self.get_parameter('require_deadman').value)
        self.deadman_button = int(self.get_parameter('deadman_button').value)
        self.publish_zero_on_release = bool(self.get_parameter('publish_zero_on_release').value)

        self.speed_scale = float(self.get_parameter('speed_scale').value)
        self.steering_scale = float(self.get_parameter('steering_scale').value)

        self.last_deadman_state = False

        self.sub = self.create_subscription(
            Joy,
            self.joy_topic,
            self.joy_callback,
            10
        )

        self.pub = self.create_publisher(
            AckermannDriveStamped,
            self.cmd_topic,
            10
        )

        self.add_on_set_parameters_callback(self.parameter_callback)

        self.get_logger().info(
            f'Started joy_ackermann_filter: {self.joy_topic} -> {self.cmd_topic}, '
            f'max_speed={self.max_speed:.3f} m/s, '
            f'max_steering_angle={self.max_steering_angle:.3f} rad, '
            f'speed_axis={self.speed_axis}, steering_axis={self.steering_axis}'
        )

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'max_speed':
                if param.value < 0.0:
                    return SetParametersResult(successful=False, reason='max_speed must be >= 0')
                self.max_speed = float(param.value)

            elif param.name == 'max_steering_angle':
                if param.value < 0.0:
                    return SetParametersResult(successful=False, reason='max_steering_angle must be >= 0')
                self.max_steering_angle = float(param.value)

            elif param.name == 'speed_scale':
                self.speed_scale = float(param.value)

            elif param.name == 'steering_scale':
                self.steering_scale = float(param.value)

            elif param.name == 'speed_sign':
                self.speed_sign = float(param.value)

            elif param.name == 'steering_sign':
                self.steering_sign = float(param.value)

            elif param.name == 'require_deadman':
                self.require_deadman = bool(param.value)

            elif param.name == 'deadman_button':
                self.deadman_button = int(param.value)

            elif param.name == 'publish_zero_on_release':
                self.publish_zero_on_release = bool(param.value)

            elif param.name == 'speed_axis':
                self.speed_axis = int(param.value)

            elif param.name == 'steering_axis':
                self.steering_axis = int(param.value)

        self.get_logger().info(
            f'Updated params: max_speed={self.max_speed:.3f}, '
            f'max_steering_angle={self.max_steering_angle:.3f}, '
            f'speed_axis={self.speed_axis}, steering_axis={self.steering_axis}, '
            f'speed_sign={self.speed_sign:.1f}, steering_sign={self.steering_sign:.1f}'
        )
        return SetParametersResult(successful=True)

    @staticmethod
    def clamp(value, min_value, max_value):
        return max(min(value, max_value), min_value)

    def publish_drive(self, speed, steering):
        msg = AckermannDriveStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id
        msg.drive.speed = float(speed)
        msg.drive.steering_angle = float(steering)
        msg.drive.acceleration = 0.0
        msg.drive.jerk = 0.0
        msg.drive.steering_angle_velocity = 0.0
        self.pub.publish(msg)

    def joy_callback(self, msg: Joy):
        if self.speed_axis >= len(msg.axes) or self.steering_axis >= len(msg.axes):
            self.get_logger().warn(
                f'Joystick axes array too small. '
                f'Configured speed_axis={self.speed_axis}, steering_axis={self.steering_axis}, '
                f'but len(axes)={len(msg.axes)}'
            )
            return

        deadman_pressed = True
        if self.require_deadman:
            if self.deadman_button >= len(msg.buttons):
                self.get_logger().warn(
                    f'Joystick buttons array too small. '
                    f'Configured deadman_button={self.deadman_button}, but len(buttons)={len(msg.buttons)}'
                )
                return
            deadman_pressed = bool(msg.buttons[self.deadman_button])

        if self.require_deadman and not deadman_pressed:
            if self.publish_zero_on_release and self.last_deadman_state:
                self.publish_drive(0.0, 0.0)
            self.last_deadman_state = False
            return

        speed_input = self.clamp(msg.axes[self.speed_axis], -1.0, 1.0)
        steering_input = self.clamp(msg.axes[self.steering_axis], -1.0, 1.0)

        speed_cmd = speed_input * self.speed_scale * self.max_speed * self.speed_sign
        steering_cmd = (
            steering_input *
            self.steering_scale *
            self.max_steering_angle *
            self.steering_sign
        )

        speed_cmd = self.clamp(speed_cmd, -self.max_speed, self.max_speed)
        steering_cmd = self.clamp(
            steering_cmd,
            -self.max_steering_angle,
            self.max_steering_angle
        )

        self.publish_drive(speed_cmd, steering_cmd)
        self.last_deadman_state = deadman_pressed


def main(args=None):
    rclpy.init(args=args)
    node = JoyAckermannFilter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()