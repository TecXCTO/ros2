# Build and Run Your Code
# Go to your workspace root, build your system, and link the configurations:

cd ~/ros2/projects/project1/ros2_ws
colcon build --packages-select tecx_robot_pkg
source install/setup.bash
# To run your code, open Terminal Terminal 1: To run your code, open Terminal Terminal 1:
source ~/ros2/projects/project1/ros2_ws/install/setup.bash
ros2 run tecx_robot_pkg talker




# Open a completely new Terminal Terminal 2:

## source ~/ros2_ws/install/setup.bash
##ros2 run my_robot_pkg listener
