#! /usr/bin/env python

import roslib
roslib.load_manifest('thesis')
import rospy
import tf
import math
import numpy
from geometry_msgs.msg import *
from std_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *


def define_plots():
  pub = rospy.Publisher('/plot_of_amcl_pose', PoseArray)
  f_amcl_pose = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/amcl_pose.txt', 'r')
  
  tl = tf.TransformListener()
  
  rospy.sleep(2.0)
  
  p = PoseArray()
  p.header.seq = 0
  p.header.frame_id = "map"
  seq = 0
  
  count_lines = 0
  for line in f_amcl_pose:
    count_lines += 1
  print 'File lines counted!'
  
  f_amcl_pose.seek(0, 0)
  for j in range(0, count_lines):
    seq += 1
    line = f_amcl_pose.readline()
    if "position" in line:
      posture = Pose()
      x = ''
      y = ''
      x_quat = ''
      y_quat = ''
      z_quat = ''
      w_quat = ''
      
      # Getting the position of the point in path
      line_x = f_amcl_pose.readline()
      for k in range(0, len(line_x) - 10):
	x = x + line_x[9 + k]
      posture.position.x = float(x)
      line_y = f_amcl_pose.readline()
      for k in range(0, len(line_y) - 10):
	y = y + line_y[9 + k]
      posture.position.y = float(y)
      
      next_line1 = f_amcl_pose.readline()
      next_line2 = f_amcl_pose.readline()
      
      # Getting the orientation of the point in path
      line_x_quat = f_amcl_pose.readline()
      for k in range(0, len(line_x_quat) - 10):
	x_quat = x_quat + line_x_quat[9 + k]
      posture.orientation.x = float(x_quat)
      line_y_quat = f_amcl_pose.readline()
      for k in range(0, len(line_y_quat) - 10):
	y_quat = y_quat + line_y_quat[9 + k]
      posture.orientation.y = float(y_quat) 
      line_z_quat = f_amcl_pose.readline()
      for k in range(0, len(line_z_quat) - 10):
	z_quat = z_quat + line_z_quat[9 + k]
      posture.orientation.z = float(z_quat)
      line_w_quat = f_amcl_pose.readline()
      for k in range(0, len(line_w_quat) - 10):
	w_quat = w_quat + line_w_quat[9 + k]
      posture.orientation.w = float(w_quat)
      
      # Setting additional parameters of the point, transforming it from /odom to /map and appending it to the PoseArray
      posture.position.z = 0.0
      p.poses.append(posture)
      print '\rProgress: ' + str(seq / float(count_lines) * 100) + '%',
      
  pub.publish(p)
  f_amcl_pose.close()
  print '\nAMCL poses published!'

if __name__ == '__main__':
  rospy.init_node('plot_amcl_node_in_rviz_node')
  define_plots()
  rospy.spin()