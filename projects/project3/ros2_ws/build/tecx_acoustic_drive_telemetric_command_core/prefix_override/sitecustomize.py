import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/root/tecxcto/ros2/projects/project3/ros2_ws/install/tecx_acoustic_drive_telemetric_command_core'
