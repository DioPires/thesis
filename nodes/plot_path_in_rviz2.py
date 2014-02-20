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
  pub = rospy.Publisher('/plot_of_path2', Path)
  f_path = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/path.txt', 'r')
  
  tl = tf.TransformListener()
  
  rospy.sleep(2.0)
  
  p = Path()
  p.header.seq = 0
  seq = 0
  transform_to_map = False
  
  count_lines = 0
  for line in f_path:
    count_lines += 1
  print 'File lines counted!'
  
  limit = float(count_lines)
  f_path.seek(0, 0)
  for j in range(0, count_lines):
    line = f_path.readline()
    if "position" in line:
      posture = PoseStamped()
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
      posture.pose.position.x = float(x)
      line_y = f_path.readline()
      for k in range(0, len(line_y) - 12):
	y = y + line_y[11 + k]
      posture.pose.position.y = float(y)
      
      next_line1 = f_path.readline()
      next_line2 = f_path.readline()
      
      # Getting the orientation of the point in path
      line_x_quat = f_path.readline()
      for k in range(0, len(line_x_quat) - 12):
	x_quat = x_quat + line_x_quat[11 + k]
      posture.pose.orientation.x = float(x_quat)
      line_y_quat = f_path.readline()
      for k in range(0, len(line_y_quat) - 12):
	y_quat = y_quat + line_y_quat[11 + k]
      posture.pose.orientation.y = float(y_quat)
      line_z_quat = f_path.readline()
      for k in range(0, len(line_z_quat) - 12):
	z_quat = z_quat + line_z_quat[11 + k]
      posture.pose.orientation.z = float(z_quat)
      line_w_quat = f_path.readline()
      for k in range(0, len(line_w_quat) - 12):
	w_quat = w_quat + line_w_quat[11 + k]
      posture.pose.orientation.w = float(w_quat)
      
      # Setting additional parameters of the point, transforming it from /odom to /map and appending it to the PoseArray
      posture.pose.position.z = 0.0
      posture.header.seq = seq
      posture.header.stamp = rospy.Time.now()
      if transform_to_map:
	posture.header.frame_id = 'map'
	p.header.frame_id = 'map'
	pose = PoseStamped()
	pose_map = PoseStamped()
	pose.header.frame_id = 'odom'
	pose.pose.position = posture.pose.position
	pose.pose.orientation = posture.pose.orientation
	pose_map = tl.transformPose('map', pose)
	#rospy.sleep(0.5)
	posture.pose.position = pose_map.pose.position
	posture.pose.orientation = pose_map.pose.orientation
      else:
	posture.header.frame_id = 'odom'
	p.header.frame_id = 'odom'
      p.poses.append(posture)
      print '\rProgress: ' + "{0:.2f}".format(seq / limit * 100) + '%',
      seq += 1
    elif seq > int(limit):
      break
      
  pub.publish(p)
  f_path.close()
  print '\nPath published!'

if __name__ == '__main__':
  rospy.init_node('plot_of_path_in_rviz_node')
  define_plots()
  rospy.spin()