import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import Imu 
from custom_messages.msg import Gamepad 
import math 

class RobotControl(Node):
    def __init__(self):
        super().__init__('robot_control_node')
        
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.imu_sub = self.create_subscription(Imu, '/imu/data_raw', self.imu_callback, 10)
        self.gamepad_sub = self.create_subscription(Gamepad, '/pad', self.gamepad_callback, 10)
        
        self.timer = self.create_timer(0.01, self.timer_callback)
        
        self.desired_yaw = 0.0 
        self.yaw_start = None 
        self.previous_yaw_imu = None 
        self.current_yaw = 0.0 
        self.overflow_counter = 0.0
        
        self.joystick_left_x = 0.0
        self.joystick_left_y = 0.0
        self.joystick_right_x = 0.0
        self.stop_btn = False 
        
        self.kp = 0.2
        self.v_max = 1.5
        self.wz_max = 1.0
        
    def imu_callback(self, msg: Imu):
        qx = msg.orientation.x 
        qy = msg.orientation.y
        qz = msg.orientation.z
        qw = msg.orientation.w 
        
        yaw_imu = self.yaw_from_quat(qx, qy, qz, qw)
        
        if self.yaw_start is None:
            self.yaw_start = yaw_imu 
            self.prev_yaw_imu = yaw_imu 
            
        difference_yaw_imu = yaw_imu - self.prev_yaw_imu
        
        if abs(difference_yaw_imu) > math.pi:
            if yaw_imu > 0.0:
                self.overflow_counter -= 1.0
            else:
                self.overflow_counter += 1.0 
                
        self.prev_yaw_imu = yaw_imu
        
        self.current_yaw = yaw_imu - self.yaw_start + 2.0 * math.pi * self.overflow_counter
        
    def gamepad_callback(self, msg: Gamepad):
        self.joystick_left_x = (128 - msg.left_analog_x)/128
        self.joystick_left_y = (128 - msg.left_analog_y)/128
        self.joystick_right_x = (128 - msg.right_analog_x)/128
        
        self.stop_btn = msg.button_x 
        
    def yaw_from_quat(slef, qx, qy, qz, qw):
        return math.atan2(2.0 * (qw * qz + qx * qy), 1.0 - 2.0 * (qy ** 2.0 + qz ** 2.0))
    
    def sign(self, x):
        if x >= 0.0: 
            return 1.0 
        else: 
            return -1.0
    
    def timer_callback(self):
        vx = self.joystick_left_x * self.v_max 
        
        if abs(vx) > self.v_max:
            vx = self.sign(vx) * self.v_max 
            
        vy = self.joystick_left_y * self.v_max
        
        if abs(vy) > self.v_max:
            vy = self.sign(vy) * self.v_max 
            
        self.desired_yaw += self.joystick_right_x * 0.01
        yaw_error = self.desired_yaw - self.current_yaw 
        wz = self.kp * yaw_error 
        
        if abs(wz) > self.wz_max:
            wz = self.sign(wz) * self.wz-max 
            
        cmd_vel_msg = Twist()
        
        if self.stop_btn: 
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.linear.y = 0.0
            cmd_vel_msg.angular.z = 0.0
        else: 
            cmd_vel_msg.linear.x = vx
            cmd_vel_msg.linear.y = vy
            cmd_vel_msg.angular.z = wz
            
        self.cmd_vel_pub.publish(cmd_vel_msg)
        self.get_logger().info(f'Publishing: Vx = {cmd_vel_msg.linear.x:.4f}, Vy = {cmd_vel_msg.linear.y:.4f}, Wz = {cmd_vel_msg.angular.z:.4f}')
        
def main(): 
    rclpy.init()
    robot_control = RobotControl()
    rclpy.spin(robot_control)
    robot_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__': 
    main()        