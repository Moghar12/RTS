import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class SonarSensorNode(Node):
    def __init__(self):
        super().__init__('sonar_sensor_node')
        self.publisher_ = self.create_publisher(Float32, 'distance', 10)
        timer_period = 0.1  # 10 Hz
        self.timer = self.create_timer(timer_period, self.read_sensor)

    def read_sensor(self):
        distance = self.get_distance()
        msg = Float32()
        msg.data = distance
        self.publisher_.publish(msg)
        self.get_logger().info(f'Distance: {distance:.2f} m')

    def get_distance(self):
        return 0.5  # Simule une valeur fixe pour l'instant

def main(args=None):
    rclpy.init(args=args)
    node = SonarSensorNode()
    rclpy.spin(node)
    rclpy.shutdown()
