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
  p.header.frame_id = 'map'
  seq = 0
  
  count_lines = 0
  for line in f_path:
    count_lines += 1
  print 'File lines counted!'
  
  limit = float(20000)
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
      if "x" in line_x:
	for k in range(0, len(line_x) - 12):
	  x = x + line_x[10 + k]
	posture.position.x = float(x)
      else:
	print 'Porcaria no x\n'
	continue
      line_y = f_path.readline()
      if "y" in line_y:
	for k in range(0, len(line_y) - 12):
	  y = y + line_y[10 + k]
	posture.position.y = float(y)
      else:
	print 'Porcaria no y\n'
	continue
      line_z = f_path.readline()
      if "z" in line_z:
	posture.position.z = 0.0
      else:
	print 'Porcaria no z\n'
	continue
      
      
      next_line = f_path.readline()
      if "orientation" not in next_line:
	continue
      
      #next_line2 = f_path.readline()
      
      # Getting the orientation of the point in path
      line_x_quat = f_path.readline()
      if "x" in line_x_quat:
	for k in range(0, len(line_x_quat) - 12):
	  x_quat = x_quat + line_x_quat[10 + k]
	posture.orientation.x = float(x_quat)
      else:
	continue
      line_y_quat = f_path.readline()
      if "y" in line_y_quat:
	for k in range(0, len(line_y_quat) - 12):
	  y_quat = y_quat + line_y_quat[10 + k]
	posture.orientation.y = float(y_quat)
      else:
	continue
      line_z_quat = f_path.readline()
      if "z" in line_z_quat:
	for k in range(0, len(line_z_quat) - 12):
	  z_quat = z_quat + line_z_quat[10 + k]
	posture.orientation.z = float(z_quat)
      else:
	continue
      line_w_quat = f_path.readline()
      if "w" in line_w_quat:
	for k in range(0, len(line_w_quat) - 12):
	  w_quat = w_quat + line_w_quat[10 + k]
	posture.orientation.w = float(w_quat)
      else:
	continue
      
      # Setting additional parameters of the point, transforming it from /odom to /map and appending it to the PoseArray
      posture.position.z = 0.0
      pose = PoseStamped()
      pose_map = PoseStamped()
      pose.header.frame_id = 'odom'
      pose.pose.position = posture.position
      pose.pose.orientation = posture.orientation
      pose_map = tl.transformPose('map', pose)
      #rospy.sleep(0.5)
      #print 'posture before\n'
      #print posture
      #print 'pose\n'
      #print pose.pose
      #print 'pose_map\n'
      #print pose_map.pose
      posture.position = pose_map.pose.position
      posture.orientation = pose_map.pose.orientation
      #print 'posture after\n'
      #print posture
      p.poses.append(posture)
      print '\rProgress: ' + str(seq / limit * 100) + '%',
      seq += 1
      #if seq % 50 == 0:
	#pub.publish(p)
    elif seq == int(limit):
      break
      
  pub.publish(p)
  f_path.close()
  print '\nPath published!'

if __name__ == '__main__':
  rospy.init_node('plot_of_path_in_rviz_node')
  define_plots()
  rospy.spin()