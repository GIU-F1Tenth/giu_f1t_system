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
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
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
    gap_follower_config = os.path.join(
        f1tenth_stack_dir, "config", "gap_follower_config.yaml"
    )
    amcl_config = os.path.join(f1tenth_stack_dir, "config", "nav2_amcl.yaml")
    pure_pursuit_config = os.path.join(
        f1tenth_stack_dir, "config", "pure_pursuit_params.yaml"
    )
    csv_config = os.path.join(f1tenth_stack_dir, "config", "csv_path_pub.yaml")
    trailing_controller_config = os.path.join(
        f1tenth_stack_dir,
        "config",
        "trailing_controller_params.yaml",
    )
    control_gateway_config = os.path.join(
        f1tenth_stack_dir,
        "config",
        "control_gateway_params.yaml",
    )
    teleop_switcher_config = os.path.join(
        f1tenth_stack_dir,
        "config",
        "teleop_switcher_params.yaml",
    )
    fsm_config = os.path.join(f1tenth_stack_dir, "config", "fsm_params.yaml")
    detection_config = os.path.join(
        f1tenth_stack_dir, "config", "detection_config.yaml"
    )
    imu_config = os.path.join(
        f1tenth_stack_dir, "config", "artemis_config.yaml"
    )
    dynamic_lookahead_config = os.path.join(
        f1tenth_stack_dir, "config", "dynamic_lookahead_pub_config.yaml"
    )
    horizon_mapper_config = os.path.join(f1tenth_stack_dir, "config", "horizon_mapper.yaml")
    dwa_config = os.path.join(f1tenth_stack_dir, "config", "dwa_config.yaml")
    kayn_config = os.path.join(
        get_package_share_directory('kayn_controller'),
        'config', 'kayn_params.yaml'
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
    gap_follower_la = DeclareLaunchArgument(
        "gap_follower_config",
        default_value=gap_follower_config,
        description="Descriptions for gap follower config",
    )
    amcl_la = DeclareLaunchArgument(
        "amcl_config",
        default_value=amcl_config,
        description="Descriptions for amcl config",
    )
    pure_pursuit_la = DeclareLaunchArgument(
        "pure_pursuit_config",
        default_value=pure_pursuit_config,
        description="Descriptions for pp config",
    )
    csv_pp_la = DeclareLaunchArgument(
        "csv_config",
        default_value=csv_config,
        description="Descriptions for csv config",
    )
    trailing_controller_la = DeclareLaunchArgument(
        "trailing_controller_config",
        default_value=trailing_controller_config,
        description="Descriptions for trailing controller config",
    )
    control_gateway_la = DeclareLaunchArgument(
        "control_gateway_config",
        default_value=control_gateway_config,
        description="Descriptions for control gateway config",
    )
    teleop_switcher_la = DeclareLaunchArgument(
        "teleop_switcher_config",
        default_value=teleop_switcher_config,
        description="Descriptions for teleop switcher config",
    )
    fsm_la = DeclareLaunchArgument(
        "fsm_config",
        default_value=fsm_config,
        description="Descriptions for fsm config",
    )
    detection_la = DeclareLaunchArgument(
        "detection_config",
        default_value=detection_config,
        description="Descriptions for detection config",
    )
    imu_la = DeclareLaunchArgument(
        "imu_config",
        default_value=imu_config,
        description="Descriptions for imu config"
    )
    dynamic_lookahead_la = DeclareLaunchArgument(
        "dynamic_lookahead_config",
        default_value=dynamic_lookahead_config,
        description="Descriptions for dynamic lookahead config",
    )
    horizon_mapper_config_la = DeclareLaunchArgument(
        "horizon_mapper_config",
        default_value=horizon_mapper_config,
        description="Horizon mapper config file",
    )
    dwa_config_la = DeclareLaunchArgument(
        "dwa_config",
        default_value=dwa_config,
        description="DWA config file",
    )
    kayn_config_la = DeclareLaunchArgument(
        "kayn_config", 
        default_value=kayn_config,
        description="Kayn config file",
    )

    ld = LaunchDescription(
        [
            joy_la,
            vesc_la,
            sensors_la,
            mux_la,
            urg_la,
            amcl_la,
            pure_pursuit_la,
            csv_pp_la,
            trailing_controller_la,
            gap_follower_la,
            control_gateway_la,
            teleop_switcher_la,
            fsm_la,
            detection_la,
            imu_la,
            dynamic_lookahead_la,
            horizon_mapper_config_la,
            dwa_config_la,
            kayn_config_la
        ]
    )

    joy_teleop_node = Node(
        package="joy_teleop",
        executable="joy_teleop",
        name="joy_teleop",
        parameters=[LaunchConfiguration("joy_config")],
    )
    pure_pursuit_node = Node(
        package="pure_pursuit",
        executable="pure_pursuit_node",
        name="pure_pursuit_node",
        parameters=[pure_pursuit_config],
        output="screen",
    )
    csv_pp_node = Node(
        package="trajectory_planning",
        executable="csv_path_pub",
        name="csv_path_pub",
        parameters=[csv_config],
        output="screen",
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
    gap_following_node = Node(
        package="gap_follower",
        executable="steering_speed_exe",
        name="gap_steering_node",
        parameters=[gap_follower_config],
    )
    trailing_controller_node = Node(
        package="trailing_controller",
        executable="trailing_controller_node",
        name="trailing_controller_node",
        parameters=[trailing_controller_config],
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
    control_gateway_node = Node(
        package="control_gateway",
        executable="control_gateway",
        name="control_gateway",
        parameters=[control_gateway_config],
    )
    teleop_switcher_node = Node(
        package="control_gateway",
        executable="teleop_switcher",
        name="teleop_switcher",
        parameters=[teleop_switcher_config],
    )
    fsm_node = Node(
        package="decision",
        executable="fsm_node",
        name="fsm_node",
        parameters=[fsm_config],
    )
    detection_node = Node(
        package="obj_detection",
        executable="detection_node",
        name="object_detection",
        parameters=[detection_config],
        output="screen",
    )
    imu_node = Node(
        package='artemis_imu_ros2',
        executable='artemis_imu_node',
        name='artemis_imu_node',
        parameters=[imu_config]
    )
    dynamic_lookahead_path_pub = Node(
        package='trajectory_planning',
        executable='dynamic_lookahead_pub_exe',
        name='dynamic_lookahead_pub_node',
        parameters=[dynamic_lookahead_config],
    )
    horizon_mapper_node = Node(
        package="horizon_mapper",
        executable="horizon_mapper_node",
        name="horizon_mapper_node",
        parameters=[horizon_mapper_config],
        output="screen",
        emulate_tty=True,
        condition=IfCondition(LaunchConfiguration("enable_horizon_mapper")),
    )
    dwa_node = Node(
        package='overtaking',
        executable='dwa_exe',
        name='dwa_ackermann_node',
        parameters=[dwa_config],
        output='screen',
        emulate_tty=True
    )
    kayn_node = Node(
        package='kayn_controller',
        executable='kayn_node',
        name='kayn_controller_node',
        parameters=[kayn_config],
        output='screen',
        emulate_tty=True,
    )
    
    pure_pursuit_start_handler = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=pure_pursuit_node,
            on_start=[gap_following_node, csv_pp_node],
        )
    )
    gap_following_start_handler = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=gap_following_node,
            on_start=[dwa_node]
        )
    )
    dwa_start_handler = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=dwa_node,
            on_start=[control_gateway_node],
        )
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
    

    # finalize
    ld.add_action(DeclareLaunchArgument("auto_start", default_value="true"))
    ld.add_action(DeclareLaunchArgument("node_name", default_value="urg_node2"))
    ld.add_action(DeclareLaunchArgument("scan_topic_name", default_value="scan"))
    ld.add_action(DeclareLaunchArgument("enable_horizon_mapper", default_value="false"))
    
    ld.add_action(joy_teleop_node)
    ld.add_action(ackermann_to_vesc_node)
    ld.add_action(vesc_to_odom_node)
    ld.add_action(vesc_driver_node)
    ld.add_action(ackermann_mux_node)
    ld.add_action(static_tf_node)
    # ld.add_action(trailing_controller_node)
    ld.add_action(teleop_switcher_node)
    ld.add_action(fsm_node)
    ld.add_action(detection_node)
    ld.add_action(pure_pursuit_start_handler)
    ld.add_action(gap_following_start_handler)
    ld.add_action(dwa_start_handler)
    ld.add_action(pure_pursuit_node)
    # ld.add_action(imu_node)
    ld.add_action(horizon_mapper_node)
    ld.add_action(dynamic_lookahead_path_pub)
    ld.add_action(kayn_node)

    ld.add_action(urg_node)
    ld.add_action(urg_node2_node_configure_event_handler)
    ld.add_action(urg_node2_node_activate_event_handler)
    ld.add_action(map_server_node)
    ld.add_action(amcl_node)
    ld.add_action(lifecycle_manager_node)

    return ld
