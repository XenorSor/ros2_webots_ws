import rclpy
from geometry_msgs.msg import Twist
from pynput import keyboard
from pynput.keyboard import Key

Distance_between_wheels = 0.1
Wheel_radius = 0.025

class Teleop:
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
        self.__listener = keyboard.Listener(on_press=self.__on_press)
        self.__listener.start()

    def __on_press(self, key):
        forward_speed = 0.0
        angular_speed = 0.0
        try:
            if key == Key.up or key.char == "w":
                forward_speed = 0.1
                angular_speed = 0.0
            elif key == Key.down or key.char == "s":
                forward_speed = -0.1
                angular_speed = 0.0
            elif key == Key.left or key.char == "a":
                forward_speed = 0.03
                angular_speed = 1.0
            elif key == Key.right or key.char == "d":
                forward_speed = 0.03
                angular_speed = -1.0
            elif key.char == ' ':
                forward_speed = 0
                angular_speed = 0
        except AttributeError:
            pass

        command_left = (forward_speed - angular_speed * Distance_between_wheels) / Wheel_radius
        command_right = (forward_speed + angular_speed * Distance_between_wheels) / Wheel_radius

        self.front_left.setVelocity(command_left)
        self.back_left.setVelocity(command_left)
        self.front_right.setVelocity(command_right)
        self.back_right.setVelocity(command_right)

    def cb_twist(self, message):
        self.target_twist = message
    
    def step(self):
        rclpy.spin_once(self.node, timeout_sec=0)
