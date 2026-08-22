#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import serial
# Requires: pip install pyserial

class ChipDataBridge(Node):
    def __init__(self):
        super().__init__('chip_data_bridge')
        self.publisher_ = self.create_publisher(Float32, 'sensor_raw_value', 10)
        
        # Connect to the USB-Serial converter plugged into your Android phone
        # Note: In Termux-Ubuntu, USB devices usually map to /dev/ttyUSB0 or /dev/ttyACM0
        try:
            self.serial_port = serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0)
            self.get_logger().info('Successfully linked to custom electronics chip!')
        except Exception as e:
            self.get_logger().error(f'Hardware connection failed: {e}')
            return

        # Create a high-speed execution loop (runs every 0.05 seconds / 20 Hz)
        self.timer = self.create_timer(0.05, self.read_hardware_loop)

    def read_hardware_loop(self):
        if self.serial_port.in_waiting > 0:
            try:
                # Read raw incoming text bytes from the old chip
                raw_line = self.serial_port.readline().decode('utf-8').strip()
                
                # Convert the raw text data into a floating-point number
                sensor_value = float(raw_line)
                
                # Publish natively into the ROS 2 ecosystem
                msg = Float32()
                msg.data = sensor_value
                self.publisher_.publish(msg)
                
            except ValueError:
                # Catch corrupt text fragments safely without crashing the node
                pass
def main(args=None):
    rclpy.init(args=args)
    node = ChipDataBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
if __name__ == '__main__':
    main()
