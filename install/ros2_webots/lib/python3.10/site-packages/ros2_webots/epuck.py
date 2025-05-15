import rclpy
from sensor_msgs.msg import Range

Distance_between_wheels = 0.1
Wheel_radius = 0.025

class WallFollowing:
    def init(self, webots_node, properties):
        self.robot = webots_node.robot

        self.max_spped = 6.28
        self.timestep = int(self.robot.getBasicTimeStep())

        self.left = self.robot.getDevice('left wheel motor')
        self.right = self.robot.getDevice('right wheel motor')
        
        self.__prox_sensor = []
        for i in range(8):
            sensor_name = 'ps' + str(i)
            self.__prox_sensor.append(self.robot.getDevice(sensor_name))
            self.__prox_sensor[i].enable(self.timestep)

        self.left.setPosition(float('inf'))
        self.left.setVelocity(0)

        self.right.setPosition(float('inf'))
        self.right.setVelocity(0)


        rclpy.init(args=None)
        self.node = rclpy.create_node('wall_follow')
    
    def step(self):
        rclpy.spin_once(self.node, timeout_sec=0)
        
        left_wall = self.__prox_sensor[5].getValue() > 80
        left_corner = self.__prox_sensor[6].getValue() > 80
        front_wall = self.__prox_sensor[7].getValue() > 80

        command_left = self.max_spped
        command_right = self.max_spped

        if front_wall:
            command_left = self.max_spped
            command_right = -self.max_spped
        else:
            if left_wall:
                command_left = self.max_spped
                command_right = self.max_spped
            else:
                command_left = self.max_spped/4
                command_right = self.max_spped
            if left_corner:
                command_left = self.max_spped
                command_right = self.max_spped/8

        self.left.setVelocity(command_left)
        self.right.setVelocity(command_right)
