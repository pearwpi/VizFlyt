"""This is a sample motion planner"""
import numpy as np

class StudentMotionPlanning:
    """
    Implements a state machine to execute a predefined movement pattern:
    1. Take off to z= m.
    2. Move forward by  m.
    3. Move backward by m.
    4. Move left by m.
    5. Move right by m.
    """
    def __init__(self):
        self.state = 0  # Start with takeoff
        self.target_positions = [
            np.array([0.0,  0.0, 0.1]),  # Takeoff to 2m height
            np.array([0.2,  0.0, 0.1]),  # Move forward 5m
            np.array([0.2, -0.2, 0.1]), # Move backward 1m; right 2m
            np.array([0.0,  0.2, 0.1]), # Move backward 0.4m
            np.array([0.0, -0.2, 0.1]),  # Move left 2m
            np.array([0.0,  0.2, 0.1]),  # move right 2m 
            np.array([0.0,  0.0, 0.0]),  # Come back to origin
        ]
        self.current_target = self.target_positions[self.state]
        self.threshold = 0.05  
        
    def update_target(self, current_pose):
        """
        Checks if the drone reached the target and updates the next waypoint.
        Args:
            current_pose: Current (x, y, z) position of the drone.
        Returns:
            Next target position (x, y, z)
        """
        distance = np.linalg.norm(self.current_target - current_pose)
        
        if distance < self.threshold and self.state < len(self.target_positions) - 1:
            self.state += 1
            self.current_target = self.target_positions[self.state]

        return self.current_target
