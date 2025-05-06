from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='state_publisher',
            parameters=[{'use_sim_time': True}],
            arguments=['urdf/simple_car.urdf'],
            output='screen'),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'simple_car', '-file', 'urdf/simple_car.urdf'],
            output='screen')
    ])
