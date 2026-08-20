#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class DiagnosticSubscriber(Node):
    def __init__(self):
        super().__init__('diagnostic_subscriber')
        
        # Subscribe to the same topic and map it to a callback function
        self.subscription = self.create_subscription(
            String,
            'robot_status',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().warning(f'Data Ingested: [{msg.data}]')

def main(args=None):
    rclpy.init(args=args)
    node = DiagnosticSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
  
y
