# Robot Operating System (ROS 2)
It is not a traditional operating system like Windows or Linux. It is a highly powerful, open-source middleware framework that provides hardware abstraction, low-level device control, message-passing, and package management. It essentially acts as the plumbing or "nervous system" for a robot, allowing different software programs (nodes) to talk to one another smoothly.
The core reason why ROS 2 was completely rewritten from the ground up to replace ROS 1 was to remove the single point of failure (the ROS Master) and introduce industrial-grade reliability, real-time control, and native security using a decentralized standard called DDS (Data Distribution Service). [1, 4, 5] 
------------------------------
## Core Applications: What Can You Do With ROS 2?
ROS 2 is used to write code that lets robots perceive their world, make decisions, and move securely.

* 
* Autonomous Mobile Robots (AMRs): Warehouses use ROS 2 to run self-driving forklifts and delivery bots.
* Autonomous Driving: Self-driving car companies use its real-time capabilities to process LiDAR and camera streams.
* Robotic Arms: Factories deploy ROS 2 for precision picking, sorting, and manufacturing tasks.
* Drone Swarms: Multi-robot communication setups rely on its decentralized networking. [5, 6] 
* 

## Future Applications of ROS 2

* 
* Space Robotics: Powering NASA rovers and next-generation planetary explorers requiring zero-fault telemetry.
* Agricultural Automation: Autonomous tractors, weeding bots, and fruit-picking machinery.
* Medical & Surgical Bots: Precision surgical systems that require zero latency and deterministic feedback loops.
* 

------------------------------
## Conceptual Architecture (The No-Graphics Framework)
To become a pro-level engineer, you must master the fundamental building blocks of ROS 2 without relying on visual simulators. Everything in ROS 2 communication relies on the following 4 pillars:
```
+-------------------------------------------------------------+

|                        ROS 2 Workspace                      |
|                                                             |
|   +------------------+             +--------------------+   |
|   |   Node 1 (Pub)   |---Topic---->|   Node 2 (Sub)     |   |
|   +------------------+             +--------------------+   |
|            |                                 ^              |
|         Request                           Response          |
|            v                                 |              |
|   +------------------+             +--------------------+   |
|   |  Client Node     |<------------|    Server Node     |   |
|   +------------------+             +--------------------+   |
+-------------------------------------------------------------+

```
* 
* Workspace: A structured directory on your computer where you build and isolate your ROS 2 code. [7, 8] 
* Package: A dedicated container inside the workspace holding your nodes, configuration files, and dependencies. [7, 9] 
* Node: A single executable process responsible for a single task (e.g., one node reads wheel encoders, another calculates path tracking). [1, 7] 
* Topics (Publish/Subscribe): Continuous, unidirectional data streams. Node A continuously broadcasts data onto a channel (Topic), and Node B reads it. Useful for streaming sensor data. [8, 10] 
* Services (Request/Reply): Synchronous, bidirectional communication. A Client node sends a request, and a Server node computes a response and sends it back. Useful for quick actions like "turn on light." [10] 
* Actions (Goal/Feedback/Result): Asynchronous, long-running tasks. A Client triggers a target goal (e.g., "drive 5 meters forward"), receives periodic feedback while the task executes, and receives a final result when finished.
* 

------------------------------
## Step-by-Step Programming: From Scratch to Expert Code
Let's build a functional, native ROS 2 Python application entirely using terminal commands and raw python code.
## Step 1: Set Up Your Workspace
Open your Linux terminal (targeting a distribution like [ROS 2 Humble](https://docs.ros.org/en/humble/index.html) or [Jazzy Jalisco](https://docs.ros.org/en/jazzy/index.html)): [3, 7] 

# Create the workspace directory structure
```
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```
# Create a clean Python package from scratch
```
ros2 pkg create --build-type ament_python tecx_robot_pkg --dependencies rclpy std_msgs
```
## Step 2: Write the Basic Python Code (Publisher Node)
Navigate into your package directory to write the publisher logic.
```
cd ~/ros2_ws/src/tecx_robot_pkg/tecx_robot_pkg
touch telemetry_pub.py
chmod +x telemetry_pub.py
```
Open telemetry_pub.py in your text editor and write the production-grade, object-oriented node structure:
```
#!/usr/bin/env python3import rclpyfrom rclpy.node import Nodefrom std_msgs.msg import String
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
```
## Step 3: Write the Subscriber Node
Create your reader script:
```
touch diagnostic_sub.py
chmod +x diagnostic_sub.py
```
Open diagnostic_sub.py and implement the reading engine:
```
#!/usr/bin/env python3import rclpyfrom rclpy.node import Nodefrom std_msgs.msg import String
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
```
## Step 4: Configure Package Manifests
You need to tell the universal compilation framework (colcon) where to find your scripts. [2, 7] 
Open ~/ros2_ws/src/tecx_robot_pkg/setup.py and modify the entry_points field to map terminal commands directly to your scripts:
```
    entry_points={
        'console_scripts': [
            'talker = my_robot_pkg.telemetry_pub:main',
            'listener = my_robot_pkg.diagnostic_sub:main',
        ],
    },
```
## Step 5: Build and Run Your Code
Go to your workspace root, build your system, and link the configurations: [2, 7] 

```
cd ~/ros2_ws
colcon build --packages-select tecx_robot_pkg
source install/setup.bash

To run your code, open Terminal Terminal 1:

source ~/ros2_ws/install/setup.bash
ros2 run my_robot_pkg talker

Open a completely new Terminal Terminal 2:

source ~/ros2_ws/install/setup.bash
ros2 run tecx_robot_pkg listener
```

------------------------------
## Pro-Level System Introspection Tools
An expert debugging flow relies completely on command-line infrastructure rather than user interfaces:

* 
* List running processes: ros2 node list
* Examine raw topic flow data: ros2 topic list
* Echo live topic streaming data: ros2 topic echo /robot_status
* Inspect structural message definitions: ros2 interface show std_msgs/msg/String
* Analyze topic frequencies & bandwidth: ros2 topic hz /robot_status
```
root@localhost:~/tecxcto/ros2/projects# cd project1
root@localhost:~/tecxcto/ros2/projects/project1# ls
README.md  ros2_ws
root@localhost:~/tecxcto/ros2/projects/project1# ros2 pkg create --build-type ament_python tecx_robot_pkg --dependencies rclpy std_msgs
going to create a new package
package name: tecx_robot_pkg
destination directory: /root/tecxcto/ros2/projects/project1
package format: 3
version: 0.0.0
description: TODO: Package description
maintainer: ['root <root@todo.todo>']
licenses: ['TODO: License declaration']
build type: ament_python
dependencies: ['rclpy', 'std_msgs']
creating folder ./tecx_robot_pkg
creating ./tecx_robot_pkg/package.xml
creating source folder
creating folder ./tecx_robot_pkg/tecx_robot_pkg
creating ./tecx_robot_pkg/setup.py
creating ./tecx_robot_pkg/setup.cfg
creating folder ./tecx_robot_pkg/resource
creating ./tecx_robot_pkg/resource/tecx_robot_pkg
creating ./tecx_robot_pkg/tecx_robot_pkg/__init__.py
creating folder ./tecx_robot_pkg/test
creating ./tecx_robot_pkg/test/test_copyright.py
creating ./tecx_robot_pkg/test/test_flake8.py
creating ./tecx_robot_pkg/test/test_pep257.py

[WARNING]: Unknown license 'TODO: License declaration'.  This has been set in the package.xml, but no LICENSE file has been created.
It is recommended to use one of the ament license identitifers:
Apache-2.0
BSL-1.0
BSD-2.0
BSD-2-Clause
BSD-3-Clause
GPL-3.0-only
LGPL-3.0-only
MIT
MIT-0
```
