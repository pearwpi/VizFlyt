class Planner:
    """
    Planner class integrating Perception and Motion Planning.
    Generates next trajectory command based on the current pose.
    """
    def __init__(self, mode, perception_module, motion_planning_module):
        self.mode = mode
        self.perception = perception_module
        self.motion_planning = motion_planning_module

    def compute_command(self, rgb_image, depth_image, current_pose):
        """
        Computes the next target position.
        Args:
            rgb_image: RGB input from camera.
            depth_image: Depth input from camera.
            current_pose: Current drone position [x, y, z].
        Returns:
            New waypoint (x, y, z).
        """

        # Process images (not used in this example)
        _ = self.perception.process_images(rgb_image, depth_image)

        # Get the next target position
        next_waypoint = self.motion_planning.update_target(current_pose)

        return next_waypoint
