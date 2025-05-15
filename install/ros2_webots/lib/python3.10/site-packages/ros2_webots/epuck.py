import rclpy

Distance_between_wheels = 0.1
Wheel_radius = 0.025

class WallFollowing:
    def init(self, webots_node, properties):
        self.robot = webots_node.robot

        self.left = self.robot.getDevice('left wheel motor')
        self.right = self.robot.getDevice('right wheel motor')
        
        self.prox_sensor = []
        for i in range(8):
            sensor_name = 'ps' + str(i)
            self.prox_sensor.append(self.robot.getDevice(sensor_name))

        self.left.setPosition(float('inf'))
        self.left.setVelocity(0)

        self.right.setPosition(float('inf'))
        self.right.setVelocity(0)

        self.max_spped = 6.28

        rclpy.init(args=None)
        self.node = rclpy.create_node('wall_follow')

    def cb_twist(self, message):
        self.target_twist = message
    
    def step(self):
        rclpy.spin_once(self.node, timeout_sec=0)

        command_left = self.max_spped
        command_right = self.max_spped

        self.left.setVelocity(command_left)
        self.right.setVelocity(command_right)
