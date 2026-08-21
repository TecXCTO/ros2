from setuptools import find_packages, setup

package_name = 'tecx_web_accessible_robotic_telemetry_server'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'web_telemetry = tecx_web_accessible_robotic_telemetry_server.telemetry_web_node:main',
            'talker = tecx_web_accessible_robotic_telemetry_server.telemetry_pub:main',
            'listener = tecx_web_accessible_robotic_telemetry_server.diagnostic_sub:main',
        ],
    },
)
