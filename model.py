import numpy as np
import main
from math import *


def revolute_joint(theta, d, a, alpha):
    # Returns the transformation frame for a standard revolute joint (theta/alpha must be radians)
    frame_array = np.mat([[cos(theta), -sin(theta), 0, a],
                          [sin(theta)*cos(alpha), cos(theta)*cos(alpha),
                           -sin(alpha), -sin(alpha)*d],
                          [sin(theta)*sin(alpha), cos(theta)*sin(alpha), cos(alpha), cos(alpha)*d],
                          [0, 0, 0, 1]])
    return frame_array


def find_frames(theta):
    #This function returns the frames of each joint relative to the world frame for the current angles of each joint.
    # First 3 joints
    frame_01 = revolute_joint(theta[0], 0, 0, 0)  # base rotation
    frame_12 = revolute_joint(theta[1], 10, 0, pi/2.0)  # arm joint 1
    frame_23 = revolute_joint(theta[2], 0, 52, 0)  # arm joint 2

    #Wrist
    frame_34 = revolute_joint(theta[3], 0, 50, 0)
    frame_45 = revolute_joint(theta[4], 11, 0, -pi/2.0)  
    frame_56 = revolute_joint(theta[5], 0, 0, -pi/2.0)  # continuous rotation
    
    #End effector from wrist
    frame_67 = revolute_joint(0,30,0,0)

    # Absolute frames are found through matrix multiplication
    frame_02 = np.matmul(frame_01, frame_12)
    frame_03 = np.matmul(frame_02, frame_23)
    frame_04 = np.matmul(frame_03, frame_34)
    frame_05 = np.matmul(frame_04, frame_45)
    frame_06 = np.matmul(frame_05, frame_56)
    frame_07 = np.matmul(frame_06, frame_67)

    frames = [frame_01, frame_02, frame_03,
              frame_04, frame_05, frame_06, frame_07]

    return frames

def xyz_reframe(pos_delta, base_theta):
    #Function takes in veloctiy commands and transforms coordiante system by rotation of base_theta
    frame10 = revolute_joint(np.deg2rad(base_theta), 0, 0, 0)
    frame10 = frame10[0:3,0:3]

    pos_reframe = np.matmul(frame10,pos_delta)
    #Returns vector of length 3
    return pos_reframe