import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/root/tecxcto/ros2/projects/project4/ros2_ws/install/tecx_raw_microcontroller_byte_stream_parser_pkg'
