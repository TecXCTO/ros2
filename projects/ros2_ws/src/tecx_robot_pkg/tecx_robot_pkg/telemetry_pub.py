#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TelemetryPublisher(Node):
    def __init__(self):
        # Initialize the node named 'telemetry_publisher'
        super().__init__('telemetry_publisher')
        
        # Create a topic named 'robot_status' with a queue size of 10
        self.publisher_ = self.create_publisher(String, 'robot_status', 10)
        
        # Define a timer that triggers a callback every 1.0 second
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.counter = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Robot Core Online. System Runtime: {self.counter} seconds.'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Broadcasting: "{msg.data}"')
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = TelemetryPublisher()
    try:
        # Keep the node running, processing events and timers
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
  
