from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():
    pkg_path = get_package_share_directory('my_car_description')
    xacro_path = os.path.join(pkg_path, 'urdf', 'simple_car.urdf.xacro')

    # Process the XACRO file into URDF
    doc = xacro.process_file(xacro_path)
    robot_description = {'robot_description': doc.toxml()}

    world_path = os.path.join(pkg_path, 'model', 'model.sdf')

    return LaunchDescription([
        # Start Gazebo
        ExecuteProcess(
            cmd=['gazebo',world_path, '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'),

        # State publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='state_publisher',
            parameters=[robot_description],
            output='screen'),

        # Spawn the robot
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'four_wheel_car', '-topic', 'robot_description'],
            output='screen'),

        

    ])
