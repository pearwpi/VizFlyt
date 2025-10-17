from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'vizflyt'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pear_group',
    maintainer_email='rkulkarni1@wpi.edu',
    description='ROS2 Package for VizFlyt : Perception-centric Pedagogical Framework For Autonomous Aerial Robots',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'fake_vicon_node = vizflyt.fake_vicon_node:main',
            'fake_vicon_node_hitl = vizflyt.fake_vicon_node_hitl:main',
            'fake_vicon_node_keyboard = vizflyt.fake_vicon_node_keyboard:main',
            'fake_drone_control_node = vizflyt.fake_drone_control_node:main', 
            'ardupilot_drone_control_node = vizflyt.ardupilot_drone_control_node:main', 
            'blender_drone_control_node = vizflyt.blender_drone_control_node:main', 
            'render_node = vizflyt.render_node:main',
            'cam_feed_node = vizflyt.cam_feed_node:main',
            'collision_detection_node = vizflyt.collision_detection_node:main',
            'quad_simulator_node = quad_simulation.quad_simulator_node:main',
            'usercode_node = drone_stack.usercode_node:main',             
        ],
    },
)
