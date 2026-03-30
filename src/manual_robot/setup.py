from setuptools import find_packages, setup
import os 

package_name = 'manual_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), ['launch/manual_robot.launch.py'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lydia-chheng',
    maintainer_email='chhenglydiacl@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'inverse_kinematic_node=manual_robot.inverse_kinematic:main',
            'robot_control=manual_robot.robot_control:main',
            'gamepad_node=manual_robot.gamepad:main'
        ],
    },
)
