#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import Image
from vicon_receiver.msg import Position
from cv_bridge import CvBridge
import numpy as np

from drone_stack.Planner import Planner
from drone_stack.StudentPerception import StudentPerception
from drone_stack.StudentPlanning import StudentMotionPlanning
from rclpy.qos import QoSProfile, ReliabilityPolicy

class StateMachines(Node):
    """
    The `StateMachines` class subscribes to RGB, depth images, and Vicon position.
    It uses perception and motion planning modules to generate real-time trajectory commands.
    """

    def __init__(self):
        super().__init__('usercode_node')

        # Update rate
        self.dt = 0.1  

        # QoS Profile to ensure best-effort communication
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            depth=10
        )

        # Subscribers to sensor data and pose
        self.position_sub = self.create_subscription(
            Position, '/vicon/VizFlyt/VizFlyt', self.position_callback, qos_profile
        )
        self.rgb_sub = self.create_subscription(
            Image, '/vizflyt/rgb_image', self.rgb_callback, qos_profile
        )
        self.depth_sub = self.create_subscription(
            Image, '/vizflyt/depth_image', self.depth_callback, qos_profile
        )

        # Publisher for trajectory setpoints
        self.trajectory_pub = self.create_publisher(Float32MultiArray, '/fake_drone/trajectory_setpoint', 10)

        # CV Bridge for image processing
        self.bridge = CvBridge()

        # Initialize Perception and Motion Planning
        perception = StudentPerception("vizflyt/drone_stack/unet_150.pth")
        motion_planning = StudentMotionPlanning()
        self.planner = Planner(mode="velocity", perception_module=perception, motion_planning_module=motion_planning)

        # Placeholder for latest sensor data
        self.current_pose = None
        self.current_rgb = None
        self.current_depth = None

        # Create ROS timer
        self.timer = self.create_timer(self.dt, self.publish_trajectory)

        self.get_logger().info("StateMachines Node Initialized")

    def position_callback(self, msg):
        """ Stores latest drone position from Vicon. """
        self.current_pose = np.array([msg.x_trans, msg.y_trans, msg.z_trans])

    def rgb_callback(self, msg):
        """ Stores latest RGB image. """
        self.current_rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    def depth_callback(self, msg):
        """ Stores latest Depth image. """
        self.current_depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

    def publish_trajectory(self):
        """
        Computes and publishes the next trajectory command.
        """
        if self.current_pose is None or self.current_rgb is None or self.current_depth is None:
            self.get_logger().info("Waiting for sensor data...")
            return

        # Compute next waypoint using Perception and Planning
        next_waypoint = self.planner.compute_command(self.current_rgb, self.current_depth, self.current_pose)
        
        # Construct trajectory message (xyz, velocity, acceleration, yaw)
        msg = Float32MultiArray()
        msg.data = [
            next_waypoint[0], next_waypoint[1], next_waypoint[2],  # Position
            0.0, 0.0, 0.0,  # Velocity (Set to zero)
            0.0, 0.0, 0.0,  # Acceleration (Set to zero)
            0.0  # Yaw (Set to zero)
        ]

        # Publish the trajectory command
        self.trajectory_pub.publish(msg)
        self.get_logger().info(f"Published Trajectory: {msg.data}")

def main():
    """ Main function to run the StateMachines node. """
    rclpy.init()
    node = StateMachines()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
