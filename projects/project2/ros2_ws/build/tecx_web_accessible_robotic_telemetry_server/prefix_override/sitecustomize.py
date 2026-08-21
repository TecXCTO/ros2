import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/root/tecxcto/ros2/projects/project2/ros2_ws/install/tecx_web_accessible_robotic_telemetry_server'
