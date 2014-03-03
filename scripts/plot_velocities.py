#! /usr/bin/env python

import roslib
roslib.load_manifest('thesis')
import rospy
import tf
import math
import numpy
import matplotlib.pyplot as plt
from geometry_msgs.msg import *
from std_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *


def define_plots():
  f_cmd_vel = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/cmd_vel.txt', 'r')
  
  #rospy.sleep(2.0)
  
  seq = 0
  v = []
  w = []
  
  count_lines = 0
  count_vel = 0
  for line in f_cmd_vel:
    count_lines += 1
    if "linear" in line:
      count_vel += 1
  print 'File lines counted!'
  
  f_cmd_vel.seek(0, 0)
  for j in range(0, count_lines):
    seq += 1
    line = f_cmd_vel.readline()
    if "linear" in line:
      posture = Pose()
      x = ''
      # Getting the position of the point in path
      line_x = f_cmd_vel.readline()
      for k in range(0, len(line_x) - 6):
	x = x + line_x[5 + k]
      v.append(float(x))
    elif "angular" in line:
      y = ''
      f_cmd_vel.readline()
      f_cmd_vel.readline()
      line_y = f_cmd_vel.readline()
      for k in range(0, len(line_y) - 6):
	y = y + line_y[5 + k]
      w.append(float(y))
      
  f_cmd_vel.close()
  plots(v, w)


def plots(v, w):
  plt.subplot(2, 1, 1)
  plt.plot(numpy.linspace(0, len(v), len(v), True, False), v)
  plt.title('Linear Velocity from Monte-Carlo tests')
  plt.ylabel('Linear velocity (m / s)')
  plt.subplot(2, 1, 2)
  plt.plot(numpy.linspace(0, len(w), len(w), True, False), w)
  plt.title('Angular Velocity from Monte-Carlo tests')
  plt.ylabel('Angular velocity (rad / s)')
  plt.show()
  
  
  
if __name__ == '__main__':
  #rospy.init_node('plot_amcl_node_in_rviz_node')
  define_plots()
  #rospy.spin()