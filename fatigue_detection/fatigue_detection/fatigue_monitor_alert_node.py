import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from playsound import playsound
import threading
import time

class FatigueMonitorSubscriber(Node):
    def __init__(self):
        super().__init__('fatigue_monitor_subscriber')
        self.subscription = self.create_subscription(
            String,
            'fatigue_events',
            self.listener_callback,
            10)
        self.subscription

        # Variables de suivi
        self.blink_count = 0
        self.yawn_count = 0
        self.fatigue_score = 0

        # Graphique
        self.fig, self.ax = plt.subplots()
        self.bar = self.ax.barh(['Fatigue'], [0], color='green')
        self.ax.set_xlim(0, 10)
        self.ax.set_xlabel('Fatigue Level')
        self.ax.set_title('Driver Fatigue Monitor')

        # Animation
        self.ani = animation.FuncAnimation(self.fig, self.update_graph, interval=500)

        # Contrôle de déclenchement du son (cooldown)
        self.last_alert_time = 0
        self.alert_cooldown = 5  # en secondes

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: "{msg.data}"')
        try:
            data = msg.data.split(',')
            self.blink_count = int(data[0].split(':')[1].strip())
            self.yawn_count = int(data[1].split(':')[1].strip())

            # Calcul du score fatigue (pondération)
            self.fatigue_score = (self.blink_count * 0.2) + (self.yawn_count * 1.0)

            # Déclenchement du son si nécessaire
            if self.fatigue_score >= 8 and time.time() - self.last_alert_time > self.alert_cooldown:
                threading.Thread(target=self.play_alert_sound).start()
                self.last_alert_time = time.time()

        except Exception as e:
            self.get_logger().error(f'Error parsing message: {e}')

    def update_graph(self, i):
        color = 'green'
        if self.fatigue_score >= 5:
            color = 'orange'
        if self.fatigue_score >= 8:
            color = 'red'

        self.bar[0].set_width(self.fatigue_score)
        self.bar[0].set_color(color)
        self.ax.set_xlim(0, max(10, self.fatigue_score + 2))

    def play_alert_sound(self):
        playsound('alert.mp3')

    def show_graph(self):
        plt.show()

def main(args=None):
    rclpy.init(args=args)
    node = FatigueMonitorSubscriber()
    try:
        node.show_graph()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
