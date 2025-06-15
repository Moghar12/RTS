import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

class EmergencyBrake(Node):
    def __init__(self):
        super().__init__('emergency_brake')
        self.declare_parameter('stop_distance', 1.9)  # Stop if distance < 0.3m
        self.stop_distance = self.get_parameter('stop_distance').get_parameter_value().double_value

        # Subscribe to sonar sensor data
        self.subscription = self.create_subscription(
            Range,
            '/sonar',  # The topic from your sonar sensor
            self.sonar_callback,
            10)
        
        # Publisher for stopping the robot
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info("Emergency Brake Node Started, waiting for sonar data...")

    def sonar_callback(self, msg):
        distance = msg.range  # Get the sonar distance from Range message
        self.get_logger().info(f"Received sonar distance: {distance:.2f}m")

        # Check if the range is valid (not inf or nan)
        if distance == float('inf'):
            self.get_logger().warn("Sonar reading is infinite - no obstacle detected")
            return
        elif distance != distance:  # Check for NaN
            self.get_logger().warn("Sonar reading is NaN - invalid reading")
            return
        elif distance < msg.min_range or distance > msg.max_range:
            self.get_logger().warn(f"Sonar reading {distance:.2f}m is out of valid range [{msg.min_range:.2f}, {msg.max_range:.2f}]")
            return

        # Emergency brake logic
        if distance < self.stop_distance:
            self.get_logger().warn(f"Obstacle too close! Distance: {distance:.2f}m < {self.stop_distance:.2f}m - Stopping robot...")
            self.stop_robot()
        else:
            self.get_logger().info(f"Safe distance: {distance:.2f}m >= {self.stop_distance:.2f}m")

    def stop_robot(self):
        stop_cmd = Twist()
        stop_cmd.linear.x = 0.0
        stop_cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(stop_cmd)

def main(args=None):
    rclpy.init(args=args)
    node = EmergencyBrake()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()