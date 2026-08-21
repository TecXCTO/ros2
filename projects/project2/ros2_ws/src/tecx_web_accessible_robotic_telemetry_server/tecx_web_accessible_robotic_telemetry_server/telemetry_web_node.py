#!/usr/bin/env python3
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from flask import Flask, jsonify

# Initialize Flash application for web hosting
app = Flask(__name__)
latest_system_data = "No status received yet."

@app.route('/api/robot/status', methods=['GET'])
def get_status():
    # Exposes your internal node variables via a clean JSON web api
    return jsonify({"status": latest_system_data})

# ADD THESE 3 LINES RIGHT HERE:
@app.route('/')
def home():
    return jsonify({"status": latest_system_data})
    
def run_flask():
    # Host on port 5000 accessible across your local network
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

class WebTelemetryBridge(Node):
    def __init__(self):
        super().__init__('web_telemetry_bridge')
        self.subscription = self.create_subscription(
            String,
            'robot_status',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        global latest_system_data
        latest_system_data = msg.data
        self.get_logger().info(f'Cached data for web view: {msg.data}')

def main(args=None):
    # Start web server thread safely in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Fire up the ROS 2 loop engine
    rclpy.init(args=args)
    node = WebTelemetryBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
  
