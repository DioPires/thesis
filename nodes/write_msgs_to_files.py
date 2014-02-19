#! /usr/bin/env python

import roslib
roslib.load_manifest('thesis')
import rospy
import math
from geometry_msgs.msg import *
from std_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *
import actionlib
import move_base_msgs.msg
import sound_play.msg

flag_ = "False"

f_amcl_pose_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/amcl_pose.txt', 'a')
f_particlecloud_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/particlecloud.txt', 'a')
f_scan_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/scan.txt', 'a')
f_pose_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/pose.txt', 'a')
f_cmd_vel_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/cmd_vel.txt', 'a')
f_path_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/path.txt', 'a')


def write2files(msg):
  global flag_
  flag_ = str(msg)
  
  if "Shutdown" in flag_:
    f_amcl_pose_.close()
    f_particlecloud_.close()
    f_scan_.close()
    f_pose_.close()
    f_cmd_vel_.close()
    f_path_.close()
    rospy.signal_shutdown('Ending writing-to-files task. Every file is closed!')

def write_amclpose_to_file(msg):
    if "True" in flag_:
	f_amcl_pose_.seek(-1, 2)
	s = str(msg) + '\n\n'
	f_amcl_pose_.write(s)
    
def write_particlecloud_to_file(msg):
    if "True" in flag_:
	f_particlecloud_.seek(-1, 2)
	s = str(msg) + '\n\n'
	f_particlecloud_.write(s)

def write_scan_to_file(msg):
    if "True" in flag_:
	f_scan_.seek(-1, 2)
	s = str(msg) + '\n\n'
	f_scan_.write(s)

def write_pose_to_file(msg):
    if "True" in flag_:
	f_pose_.seek(-1, 2)
	s = str(msg) + '\n\n'
	f_pose_.write(s)

def write_cmd_vel_to_file(msg):
    if "True" in flag_:
	f_cmd_vel_.seek(-1, 2)
	s = str(msg) + '\n\n'
	f_cmd_vel_.write(s)  
  
def write_path_to_file(msg):
    if "True" in flag_:
	f_path_.seek(-1, 2)
	s = str(msg) + '\n\n'
	f_path_.write(s)

if __name__ == '__main__':
  rospy.init_node('write2files_node')
  rospy.Subscriber('/write_to_files', String, write2files)
  rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, write_amclpose_to_file)
  rospy.Subscriber('/particlecloud', PoseArray, write_particlecloud_to_file)
  rospy.Subscriber('/scan', LaserScan, write_scan_to_file)
  rospy.Subscriber('/pose', Odometry, write_pose_to_file)
  rospy.Subscriber('/cmd_vel', Twist, write_cmd_vel_to_file)
  rospy.Subscriber('/move_base/TrajectoryPlannerROS/global_plan', Path, write_path_to_file)
  rospy.spin()