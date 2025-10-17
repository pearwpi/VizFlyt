"""
This script reads a CSV file containing a predefined drone trajectory 
and executes it. 

Users can modify this script to:
- Subscribe to RGB and depth image topics.
- Implement Perception and Motion Planning.
- Process sensor data and generate new movement commands.

The drone's movement can be recorded after running the fake Vicon node.
"""

import numpy as np

class StateMachines:
    """
    The `StateMachines` class generates position, velocity, and acceleration 
    commands for simulating drone movement. 

    It reads a trajectory from a CSV file and steps through it, providing 
    waypoints sequentially
    """
    
    def __init__(self):    
        self.dt = 0.1
        self.MP = np.genfromtxt(
            fname="vizflyt/quad_simulation/traj/MP.csv",
            delimiter=',',
            skip_header=0,
        )
        self.active_index = 0
        self.max_index = self.MP.shape[1]
        
    def step(self, time, current_pose, current_velocity):
        """
        Retrieves the next setpoint in the trajectory.

        Args:
            time (float): The current simulation time.
            current_pose (numpy array): The drone's current position (x, y, z).
            current_velocity (numpy array): The drone's current velocity (vx, vy, vz).

        Returns:
            tuple: (xyz_desired, vel_desired, acc_desired, yaw_setpoint)
                - xyz_desired (numpy array): Target position [x, y, z].
                - vel_desired (numpy array): Target velocity [vx, vy, vz].
                - acc_desired (numpy array): Target acceleration [ax, ay, az].
                - yaw_setpoint (float): Desired yaw angle (currently set to 0).
        """   
        if (self.active_index >= self.max_index):
            
            self.active_index = self.max_index -1 
                    
        xyz_desired = self.MP[:3, self.active_index]
        vel_desired = self.MP[3:6, self.active_index] 
        acc_desired = self.MP[6:, self.active_index] 
        yaw_setpoint = 0.0
        
        self.active_index += 1
                
        return xyz_desired, vel_desired, acc_desired, yaw_setpoint

