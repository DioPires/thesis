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
  pub = rospy.Publisher('/plot_of_path', PoseArray)
  f_path = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/path.txt', 'r')
  
  tl = tf.TransformListener()
  
  rospy.sleep(2.0)
  
  p = PoseArray()
  p.header.seq = 0
  p.header.frame_id = 'odom'
  seq = 0
  limit = float(50000)
  
  count_lines = 0
  for line in f_path:
    count_lines += 1
  print 'File lines counted!'
  
  f_path.seek(0, 0)
  for j in range(0, count_lines):
    line = f_path.readline()
    if "position" in line:
      posture = Pose()
      x = ''
      y = ''
      x_quat = ''
      y_quat = ''
      z_quat = ''
      w_quat = ''
      
      # Getting the position of the point in path
      line_x = f_path.readline()
      for k in range(0, len(line_x) - 12):
	x = x + line_x[11 + k]
      posture.position.x = float(x)
      line_y = f_path.readline()
      for k in range(0, len(line_y) - 12):
	y = y + line_y[11 + k]
      posture.position.y = float(y)
      
      next_line1 = f_path.readline()
      next_line2 = f_path.readline()
      
      # Getting the orientation of the point in path
      line_x_quat = f_path.readline()
      for k in range(0, len(line_x_quat) - 12):
	x_quat = x_quat + line_x_quat[11 + k]
      posture.orientation.x = float(x_quat)
      line_y_quat = f_path.readline()
      for k in range(0, len(line_y_quat) - 12):
	y_quat = y_quat + line_y_quat[11 + k]
      posture.orientation.y = float(y_quat)
      line_z_quat = f_path.readline()
      for k in range(0, len(line_z_quat) - 12):
	z_quat = z_quat + line_z_quat[11 + k]
      posture.orientation.z = float(z_quat)
      line_w_quat = f_path.readline()
      for k in range(0, len(line_w_quat) - 12):
	w_quat = w_quat + line_w_quat[11 + k]
      posture.orientation.w = float(w_quat)
      
      # Setting additional parameters of the point, transforming it from /odom to /map and appending it to the PoseArray
      posture.position.z = 0.0
      #pose = PoseStamped()
      #pose_map = PoseStamped()
      #pose.header.frame_id = 'odom'
      #pose.pose.position = posture.position
      #pose.pose.orientation = posture.orientation
      #pose_map = tl.transformPose('map', pose)
      #rospy.sleep(0.5)
      #posture.position = pose_map.pose.position
      #posture.orientation = pose_map.pose.orientation
      p.poses.append(posture)
      print '\rProgress: ' + str(seq / limit * 100) + '%',
      seq += 1
    elif seq == int(limit):
      break
      
  pub.publish(p)
  f_path.close()
  print '\nPath published!'

if __name__ == '__main__':
  rospy.init_node('plot_of_path_in_rviz_node')
  define_plots()
  rospy.spin()