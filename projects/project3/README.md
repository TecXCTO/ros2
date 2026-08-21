------------------------------
## Project Name: Acoustic-Drive Telemetric Command Core (ADTCC)
This custom project turns your Bluetooth Headphones and a low-cost, Wi-Fi/Bluetooth-enabled microcontroller (like an ESP32 or Raspberry Pi Pico W) into a completely voice-guided or button-triggered mobile robotic control hub.
## System Architecture Overview
Instead of standard graphics packages, your phone sits in the middle as the high-speed computational brain, bridging your audio inputs and physical motors:
```
[ Bluetooth Headphone ] 
       │ (Microphone / Button Press Events)
       ▼
[ Phone Hardware Layer ] ──(Termux App/Ubuntu)──► [ ROS 2 Core Logic Node ]
                                                        │
                                                        │ (Wi-Fi WebSocket / UDP Data)
                                                        ▼
                                                 [ ESP32 Microcontroller ]
                                                        │
                                                        ▼
                                                 [ DC Motors / Robot Chassis ]
```
------------------------------
## In-Depth Explanation: How It Works## 1. The Input Layer (Your Bluetooth Headphone)
Your Bluetooth headphones act as the primary human-robot interface. You can leverage them in two ways:

* Voice Ingestion: You speak commands into the headphone's built-in microphone (e.g., "Move Forward", "Stop"). A lightweight python script in Termux captures this audio stream.
* Media Button Interception: You click the Play/Pause or Volume Up/Down physical buttons on your headphones. These trigger raw keypress events inside the Linux environment.

## 2. The Compute Layer (Termux + Ubuntu ROS 2)
Your phone handles the heavy algorithmic lifting that standard microcontrollers cannot perform:

* Audio-to-Command Processing: It converts the voice or button actions into raw text parameters.
* ROS 2 Node Serialization: A dedicated ROS 2 Node maps these inputs into standard ROS 2 messaging structures—specifically a geometry_msgs/msg/Twist data type (the industry standard for moving robots, which contains directional speeds linear.x and angular.z).

## 3. The Physical Output Layer (ESP32 via Wi-Fi/Bluetooth)
An ESP32 is a small $5 microchip containing built-in Wi-Fi and Bluetooth. It handles the physical world:

* It connects to your phone's mobile hotspot or your home Wi-Fi network.
* It hosts a micro-listener script (using raw UDP sockets or Micro-ROS).
* When it receives the motion message from your phone, it toggles its physical hardware pins (GPIO) to drive a motor driver board, turning the wheels of a custom desktop toy car.

------------------------------
## Step-by-Step Code Implementation
Let's build the core Headless Command Node that translates keyboard inputs (simulating headphone button triggers) into real robot movement data streams, ready to be sent over your local network.
## Step 1: Install Data Dependencies
Ensure your ROS 2 system has the core geometry message definitions installed inside your Ubuntu environment:
```
sudo apt update
sudo apt install ros-humble-geometry-msgs python3-pip -y
```
### Step-by-Step Programming: 
From Scratch to Expert Code

let's build a functional, native ROS 2 Python application entirely using terminal commands and raw python code.

#### Step 1a: Set Up Your Workspace
Open your Linux terminal (targeting a distribution like ROS 2 Humble or Jazzy Jalisco):
```
# Create the workspace directory structure
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Create a clean Python package from scratch
ros2 pkg create --build-type ament_python tecx_acoustic_drive_telemetric_command_core --dependencies rclpy std_msgs
```

#### Step 1.b: Write the Basic Python Code (Publisher Node)Navigate into your package directory to write the publisher logic.
```
cd ~/ros2_ws/src/tecx_acoustic_drive_telemetric_command_core/tecx_acoustic_drive_telemetric_command_core
touch headphone_teleop_node.py
chmod +x headphone_teleop_node.py
```
## Step 2: Write the Central Brain Logic Node

Create a file named headphone_teleop_node.py inside your ROS 2 package workspace. This node takes button/text inputs and continuously broadcasts movement velocities.
```
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
```
## Step 3: Compile and Test the Core Data Feed
```
# 1.
Run colcon build --packages-select your_package_name at the root of your workspace (~/ros2_ws).
   2. Run the node: ros2 run your_package_name headline_teleop
   3. Press w, a, s, or d inside your Termux terminal window.
   4. Open a completely separate terminal tab in Termux-Ubuntu and inspect the real structural data flowing through your system by typing:
   
   ros2 topic echo /cmd_vel
 ```  
   You will see the exact linear and angular vector matrices changing in real-time instantly based on your commands.

------------------------------
## Moving to the Next Level: The Network Hook
To pass this data out of your phone to an external microcontroller (like an ESP32), you can write a tiny companion script inside your package that reads this /cmd_vel data and outputs it via a standard Python network socket over Wi-Fi.
