import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

class EmergencyBrake(Node):
    def __init__(self):
        super().__init__('emergency_brake')
        self.declare_parameter('stop_distance', 0.3)  # Stop if distance < 0.3m
        self.stop_distance = self.get_parameter('stop_distance').get_parameter_value().double_value

        # Subscribe to sonar sensor data
        self.subscription = self.create_subscription(
            Float32,
            'distance',  # The topic from your sonar node
            self.sonar_callback,
            10)
        
        # Publisher for stopping the robot
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info("Emergency Brake Node Started, waiting for sonar data...")

    def sonar_callback(self, msg):
        distance = msg.data  # Get the sonar distance
        self.get_logger().info(f"Received sonar distance: {distance:.2f}m")

        if distance < self.stop_distance:
            self.get_logger().warn("Obstacle too close! Stopping robot...")
            self.stop_robot()

    def stop_robot(self):
        stop_cmd = Twist()
        stop_cmd.linear.x = 0.0
        stop_cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(stop_cmd)

def main(args=None):
    rclpy.init(args=args)
    node = EmergencyBrake()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
