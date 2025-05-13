import os
import launch
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
import launch.event_handlers
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController
from launch_ros.actions import Node

def generate_launch_description():
    package_dir = get_package_share_directory('ros2_webots')
    robot_description_path = os.path.join(package_dir, 'resource', 'car_with_sensors.urdf')

    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'car_2.wbt')
    )

    my_robot_driver = WebotsController(
        robot_name='car',
        parameters=[
            {'robot_description': robot_description_path}
        ],
        respawn=True
    )

    obstacle_avoider = Node(
        package='ros2_webots',
        executable='obstacle_avoider'
    )

    return LaunchDescription([
        webots,
        my_robot_driver,
        obstacle_avoider,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())]
            )
        )
    ])