# manual_robot_ws

A ROS 2 source file for manual robot control

## Features

- Heading Hold: Uses IMU feedback to keep the robot driving straight even with external disturbances.
- Mecanum/Omni Kinematics: Translates high-level velocity commands ($V_x, V_y, W_z$) into individual motor speeds.
- Safety Switch: Integrated emergency stop via the gamepad 'X' button.

## Project Structure

- `manual_robot/`: Contains the core Python logic.
  - `robot_control.py`: The "Brain" – handles gamepad input and PID heading control.
  - `inverse_kinematic.py`: The "Translator" – converts velocity to motor commands.
- `launch/`: Contains `manual_robot.launch.py` to start all nodes at once.
- `custom_messages/`: Definintions for `EncoderFeedback` and `Gamepad` messages and other `.msg` files.
- `can_driver/`: Contains CAN sender and receiver file `can_driver.py` that enables communication between ROS 2 and smart driver.
- `hfi_a9/`: Contains IMU reading file `hfi_a9` that publishes IMU data to other nodes.

## Configuration

1. Build the Workspace
Ensure you are in the root of your workspace (`manual_robot_ws`).

``` bash
colcon build
source install/setup.bash
```

2. Run the packages

Launch the control system and kinematics together:

``` bash
ros2 run can_driver can_driver_node
ros2 run hfi_a9 hfi_a9_node
ros2 launch manual_robot manual_robot.launch.py
```

3. Verify Communication

To see the commands being sent to the motors in real-time, open a new terminal and run:

``` bash
ros2 topic echo /publish_motor
```

## Control Mapping

- Left Joystick: Linear movement ($V_x$ and $V_y$).
- Right Joystick (X-axis): Sets the Desired Yaw (turning the robot).
- Button X: Emergency Stop (Zeroes all velocities).

## Key Concepts

- Topics: The Gamepad App Publishes to `/pad`, and the `RobotControl` node Subscribes to it.
- Heading Hold: The robot calculates the error between where it wants to face and its current IMU reading to stay stable.
- Kinematics: The math that ensures all four wheels work together to move in the intended direction.
