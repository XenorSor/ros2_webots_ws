import rclpy
from geometry_msgs.msg import Twist

Distance_between_wheels = 0.1
Wheel_radius = 0.025

class CarDriver:
    def init(self, webots_node, properties):
        self.robot = webots_node.robot

        self.front_left = self.robot.getDevice('front left')
        self.front_right = self.robot.getDevice('front right')
        self.back_left = self.robot.getDevice('back left')
        self.back_right = self.robot.getDevice('back right')

        self.front_left.setPosition(float('inf'))
        self.front_left.setVelocity(0)

        self.front_right.setPosition(float('inf'))
        self.front_right.setVelocity(0)

        self.back_left.setPosition(float('inf'))
        self.back_left.setVelocity(0)

        self.back_right.setPosition(float('inf'))
        self.back_right.setVelocity(0)

        self.target_twist = Twist()

        rclpy.init(args=None)
        self.node = rclpy.create_node('car_driver')
        self.node.create_subscription(Twist, 'cmd_vel', self.cb_twist, 1)

    def cb_twist(self, message):
        self.target_twist = message
    
    def step(self):
        rclpy.spin_once(self.node, timeout_sec=0)
        
        forward_speed = self.target_twist.linear.x
        angular_speed = self.target_twist.angular.z

        command_left = (forward_speed - angular_speed * Distance_between_wheels) / Wheel_radius
        command_right = (forward_speed + angular_speed * Distance_between_wheels) / Wheel_radius

        self.front_left.setVelocity(command_left)
        self.back_left.setVelocity(command_left)
        self.front_right.setVelocity(command_right)
        self.back_right.setVelocity(command_right)
