import os
import launch
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
import launch.event_handlers
from webots_ros2_driver.webots_launcher import WebotsLauncher

def generate_launch_description():
    package_dir = get_package_share_directory('ros2_webots')

    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'car_1.wbt')
    )

    return LaunchDescription([
        webots,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())]
            )
        )
    ])