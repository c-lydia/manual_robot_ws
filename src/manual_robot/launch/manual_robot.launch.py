import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'manual_robot'

    return LaunchDescription([
        Node(
            package=package_name,
            executable='robot_control',
            name='robot_control_node',
            output='screen'
        ),

        Node(
            package=package_name,
            executable='inverse_kinematic',
            name='inverse_kinematics_node',
            output='screen'
        ),
        
        Node(
            package=package_name,
            executable='gamepad',
            name='gamepad_node', 
            output='screen'
        )
    ])