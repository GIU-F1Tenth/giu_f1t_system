# MIT License

# Copyright (c) 2025 Hongrui Zheng

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
from launch.conditions import IfCondition
from launch_ros.actions import LifecycleNode
from launch.actions import DeclareLaunchArgument, EmitEvent, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.events import matches_action
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition


def generate_launch_description():
    f1tenth_stack_dir = get_package_share_directory("f1tenth_stack")
    joy_teleop_config = os.path.join(f1tenth_stack_dir, "config", "joy_teleop.yaml")
    vesc_config = os.path.join(f1tenth_stack_dir, "config", "vesc.yaml")
    sensors_config = os.path.join(f1tenth_stack_dir, "config", "sensors.yaml")
    mux_config = os.path.join(f1tenth_stack_dir, "config", "mux.yaml")
    urg_config = os.path.join(f1tenth_stack_dir, "config", "params_ether.yaml")
    map_server_config = os.path.join(f1tenth_stack_dir, "maps", "map.yaml")
    amcl_config = os.path.join(f1tenth_stack_dir, "config", "nav2_amcl.yaml")
    lqr_config = os.path.join(f1tenth_stack_dir, "config", "lqr_params.yaml")
    horizon_mapper_config = os.path.join(f1tenth_stack_dir, "config", "horizon_mapper.yaml")
    lqr_config = os.path.join(f1tenth_stack_dir, "config", "lqr_params.yaml")
    control_gateway_config = os.path.join(
        f1tenth_stack_dir,
        "config",
        "control_gateway_params.yaml",
    )

    joy_la = DeclareLaunchArgument(
        "joy_config",
        default_value=joy_teleop_config,
        description="Descriptions for joy and joy_teleop configs",
    )
    vesc_la = DeclareLaunchArgument(
        "vesc_config",
        default_value=vesc_config,
        description="Descriptions for vesc configs",
    )
    sensors_la = DeclareLaunchArgument(
        "sensors_config",
        default_value=sensors_config,
        description="Descriptions for sensor configs",
    )
    mux_la = DeclareLaunchArgument(
        "mux_config",
        default_value=mux_config,
        description="Descriptions for ackermann mux configs",
    )
    urg_la = DeclareLaunchArgument(
        "urg_config",
        default_value=urg_config,
        description="Descriptions for urg config",
    )
    amcl_la = DeclareLaunchArgument(
        "amcl_config",
        default_value=amcl_config,
        description="Descriptions for amcl config",
    )
    lqr_config_la = DeclareLaunchArgument(
        "lqr_config",
        default_value=lqr_config,
        description="LQR controller config file",
    )
    horizon_mapper_config_la = DeclareLaunchArgument(
        "horizon_mapper_config",
        default_value=horizon_mapper_config,
        description="Horizon mapper config file",
    )
    enable_lqr_la = DeclareLaunchArgument(
        "enable_lqr",
        default_value="true",
        description="Launch the lqr_controller stack",
    )
    enable_horizon_mapper_la = DeclareLaunchArgument(
        "enable_horizon_mapper",
        default_value="false",
        description="Launch standalone horizon_mapper node",
    )
    control_gateway_la = DeclareLaunchArgument(
        "control_gateway_config",
        default_value=control_gateway_config,
        description="Descriptions for control gateway config",
    )
  
    
    ld = LaunchDescription(
        [
            joy_la,
            vesc_la,
            sensors_la,
            mux_la,
            urg_la,
            amcl_la,
            lqr_config_la,
            horizon_mapper_config_la,
            enable_lqr_la,
            enable_horizon_mapper_la,
            control_gateway_la,
        ]
    )


    horizon_mapper_launch = Node(
        package="horizon_mapper",
        executable="horizon_mapper_node",
        name="horizon_mapper_node",
        parameters=[LaunchConfiguration("horizon_mapper_config")],
        output="screen",
        emulate_tty=True,
        condition=IfCondition(LaunchConfiguration("enable_horizon_mapper")),
    )

    joy_teleop_node = Node(
        package="joy_teleop",
        executable="joy_teleop",
        name="joy_teleop",
        parameters=[LaunchConfiguration("joy_config")],
    )
    ackermann_to_vesc_node = Node(
        package="vesc_ackermann",
        executable="ackermann_to_vesc_node",
        name="ackermann_to_vesc_node",
        parameters=[LaunchConfiguration("vesc_config")],
    )
    vesc_to_odom_node = Node(
        package="vesc_ackermann",
        executable="vesc_to_odom_node",
        name="vesc_to_odom_node",
        parameters=[LaunchConfiguration("vesc_config")],
    )
    vesc_driver_node = Node(
        package="vesc_driver",
        executable="vesc_driver_node",
        name="vesc_driver_node",
        parameters=[LaunchConfiguration("vesc_config")],
    )
    urg_node = LifecycleNode(
        package="urg_node2",
        executable="urg_node2_node",
        name=LaunchConfiguration("node_name"),
        remappings=[("scan", LaunchConfiguration("scan_topic_name"))],
        parameters=[LaunchConfiguration("urg_config")],
        namespace="",
        output="screen",
    )
    ackermann_mux_node = Node(
        package="ackermann_mux",
        executable="ackermann_mux",
        name="ackermann_mux",
        parameters=[LaunchConfiguration("mux_config")],
        remappings=[("ackermann_cmd_out", "ackermann_drive")],
    )
    static_tf_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_baselink_to_laser",
        arguments=["0.27", "0.0", "0.11", "0.0", "0.0", "0.0", "base_link", "laser"],
    )
    map_server_node = LifecycleNode(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[{"yaml_filename": map_server_config}],
        namespace="",
    )
    amcl_node = LifecycleNode(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[LaunchConfiguration("amcl_config")],
        namespace="",
    )
    lifecycle_manager_node = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_map",
        output="screen",
        parameters=[
            {
                "use_sim_time": False,
                "autostart": True,
                "node_names": ["map_server", "amcl"],
            }
        ],
    )

    urg_node2_node_configure_event_handler = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=urg_node,
            on_start=[
                EmitEvent(
                    event=ChangeState(
                        lifecycle_node_matcher=matches_action(urg_node),
                        transition_id=Transition.TRANSITION_CONFIGURE,
                    ),
                ),
            ],
        ),
        condition=IfCondition(LaunchConfiguration("auto_start")),
    )

    urg_node2_node_activate_event_handler = RegisterEventHandler(
        event_handler=OnStateTransition(
            target_lifecycle_node=urg_node,
            start_state="configuring",
            goal_state="inactive",
            entities=[
                EmitEvent(
                    event=ChangeState(
                        lifecycle_node_matcher=matches_action(urg_node),
                        transition_id=Transition.TRANSITION_ACTIVATE,
                    ),
                ),
            ],
        ),
        condition=IfCondition(LaunchConfiguration("auto_start")),
    )
    control_gateway_node = Node(
        package="control_gateway",
        executable="control_gateway",
        name="control_gateway",
        parameters=[control_gateway_config],
    )
    lqr_controller_node = Node(
        package='lqr_controller',
        executable='lqr_node',
        name='adaptive_lqr_controller_node',
        parameters=[lqr_config],
        emulate_tty=True,
    )
    horizon_mapper_node = Node(
        package='horizon_mapper',
        executable='horizon_mapper_node',
        name='horizon_mapper_node',
        parameters=[horizon_mapper_config],
        emulate_tty=True, 
    )

    # finalize
    ld.add_action(joy_teleop_node)
    ld.add_action(ackermann_to_vesc_node)
    ld.add_action(vesc_to_odom_node)
    ld.add_action(vesc_driver_node)
    ld.add_action(ackermann_mux_node)
    ld.add_action(static_tf_node)
    ld.add_action(control_gateway_node)
    #ld.add_action(lqr_controller_node)
    ld.add_action(horizon_mapper_node)

    ld.add_action(DeclareLaunchArgument("auto_start", default_value="true"))
    ld.add_action(DeclareLaunchArgument("node_name", default_value="urg_node2"))
    ld.add_action(DeclareLaunchArgument("scan_topic_name", default_value="scan"))
    ld.add_action(urg_node)
    ld.add_action(urg_node2_node_configure_event_handler)
    ld.add_action(urg_node2_node_activate_event_handler)
    ld.add_action(map_server_node)
    ld.add_action(amcl_node)
    ld.add_action(lifecycle_manager_node)
    ld.add_action(horizon_mapper_launch)

    return ld
