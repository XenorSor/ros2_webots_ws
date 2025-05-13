import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

MAX_RANGE = 0.15

class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')

        self.__publisher = self.create_publisher(Twist, 'cmd_vel', 1)

        self.create_subscription(Range, 'left_sensor', self.__left_sensor_callback, 1)
        self.create_subscription(Range, 'right_sensor', self.__right_sensor_callback, 1)
        self.create_subscription(Range, 'middle_sensor', self.__middle_sensor_callback, 1)

        self.__left_sensor_value = MAX_RANGE
        self.__right_sensor_value = MAX_RANGE
        self.__middle_sensor_value = MAX_RANGE

        self.create_timer(0.02, self.control_loop)

    def __left_sensor_callback(self, message):
        self.__left_sensor_value = message.range
    
    def __middle_sensor_callback(self, message):
        self.__middle_sensor_value = message.range
    
    def __right_sensor_callback(self, message):
        self.__right_sensor_value = message.range

    
    def control_loop(self):
        command_message = Twist()

        if self.__middle_sensor_value < 0.9 * MAX_RANGE:
            command_message.angular.z = 1.0
            command_message.linear.x = -0.03
        elif self.__left_sensor_value < 0.9 * MAX_RANGE:
            command_message.angular.z = -1.0
            command_message.linear.x = 0.03
        elif self.__right_sensor_value < 0.9 * MAX_RANGE:
            command_message.angular.z = 1.0
            command_message.linear.x = 0.03
        else:
            command_message.angular.z = 0.0
            command_message.linear.x = 0.12
        
        self.__publisher.publish(command_message)

def main(args=None):
    rclpy.init(args=args)
    avoider = ObstacleAvoider()
    rclpy.spin(avoider)
    avoider.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()