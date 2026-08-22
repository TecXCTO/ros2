#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import select
import tty
import termios

class HeadphoneTeleop(Node):
    def __init__(self):
        super().__init__('headphone_teleop_node')
        
        # Publish to standard cmd_vel topic used by physical robots
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.get_logger().info('--- Acoustic Teleop Engine Initiated ---')
        self.get_logger().info('Simulating headphone triggers via keyboard (W=Forward, S=Stop, A=Left, D=Right)')
        
        # Save terminal settings to read raw individual keystrokes cleanly
        self.settings = termios.tcgetattr(sys.stdin)

    def get_key(self):
        # Reads raw terminal button hits without waiting for the "Enter" key
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0.1)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def run_loop(self):
        twist = Twist()
        try:
            while rclpy.ok():
                key = self.get_key()
                
                # Evaluate inputs (Map these later to voice tools or hardware buttons)
                if key == 'w':
                    twist.linear.x = 0.5   # Move forward at 0.5 m/s
                    twist.angular.z = 0.0
                    self.get_logger().info('Command Issued: [LINEAR FORWARD]')
                elif key == 's':
                    twist.linear.x = 0.0   # Full abrupt halt
                    twist.angular.z = 0.0
                    self.get_logger().info('Command Issued: [EMERGENCY STOP]')
                elif key == 'a':
                    twist.linear.x = 0.2
                    twist.angular.z = 1.0  # Turn left
                    self.get_logger().info('Command Issued: [STEER LEFT]')
                elif key == 'd':
                    twist.linear.x = 0.2
                    twist.angular.z = -1.0 # Turn right
                    self.get_logger().info('Command Issued: [STEER RIGHT]')
                
                # Check for exit breakout key (Ctrl+C or 'q')
                if key == 'q':
                    break

                # Broadcast the message into the ROS 2 ecosystem
                self.publisher_.publish(twist)
                
        except Exception as e:
            self.get_logger().error(f'Error encountered in loop: {e}')
        finally:
            # Safe reset: stop any active robot moving if the node crashes
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = HeadphoneTeleop()
    
    # Run our manual control engine loop
    node.run_loop()
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
