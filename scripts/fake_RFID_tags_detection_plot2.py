#! /usr/bin/env python

import roslib
roslib.load_manifest('thesis')
import rospy
import tf
import math
import numpy
import scipy.stats
import matplotlib.pyplot as plt
from geometry_msgs.msg import *
from std_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *

time_r = []
x_r = []
y_r = []
tag_r = []
time_m = []
x_m = []
y_m = []
tag_m = []
  
def get_data_from_robot():
  global time_r
  global x_r
  global y_r
  global tag_r
  
  f = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/RFID/tag_detection_for_manual_checking2.txt', 'r')

  count_lines = 0
  for line in f:
    count_lines += 1
  #print 'File lines counted!'
  
  f.seek(0, 0)
  for j in range(0, count_lines):
    line = f.readline()
    if "Tag" in line:
      t = ''
      x = ''
      y = ''
      tag_r.append(int(line[4]))
      line = f.readline()
      for k in range(0, len(line)):
	t += line[k]
      time_r.append(int(t))
      line = f.readline()
      line = f.readline()
      for k in range(0, len(line) - 6):
	x += line[5 + k]
      x_r.append(float(x))
      line = f.readline()
      for k in range(0, len(line) - 6):
	y += line[5 + k]
      y_r.append(float(y))

  tag0 = 0
  tag1 = 0
  tag2 = 0
  for k in range(0, len(tag_r)):
    if tag_r[k] == 0:
      tag0 += 1
    elif tag_r[k] == 1:
      tag1 += 1
    elif tag_r[k] == 2:
      tag2 += 1

  #print tag0
  #print tag1
  #print tag2
  
  
def get_data_from_manual_check():
  global time_m
  global x_m
  global y_m
  global tag_m
  
  f = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/RFID/manual_tag_detection2.txt', 'r')

  count_lines = 0
  for line in f:
    count_lines += 1
  #print 'File lines counted!'
  
  cnt = 0
  f.seek(0, 0)
  for j in range(0, count_lines):
    if cnt >= count_lines - 2:
      break
    elif cnt == 0:
      t = ''
      x = ''
      y = ''
      line = f.readline()
      line = f.readline()
      tag_m.append(int(line))
      line = f.readline()
      for k in range(0, len(line)):
	t += line[k]
      time_m.append(long(line))
      line = f.readline()
      line = f.readline()
      for k in range(0, len(line) - 6):
	x += line[5 + k]
      x_m.append(float(x))
      line = f.readline()
      for k in range(0, len(line) - 6):
	y += line[5 + k]
      y_m.append(float(y))
      cnt += 12
    else:
      line = f.readline()
      if "---" in line:
	t = ''
	x = ''
	y = ''
	line = f.readline()
	tag_m.append(int(line))
	line = f.readline()
	for k in range(0, len(line)):
	  t += line[k]
	time_m.append(long(line))
	line = f.readline()
	line = f.readline()
	for k in range(0, len(line) - 6):
	  x += line[5 + k]
	x_m.append(float(x))
	line = f.readline()
	for k in range(0, len(line) - 6):
	  y += line[5 + k]
	y_m.append(float(y))
	cnt += 12

  tag0 = 0
  tag1 = 0
  tag2 = 0
  for k in range(0, len(tag_m)):
    if tag_m[k] == 0:
      tag0 += 1
    elif tag_m[k] == 1:
      tag1 += 1
    elif tag_m[k] == 2:
      tag2 += 1

  #print tag0
  #print tag1
  #print tag2
      
  
def plots():
  M = numpy.zeros(6).reshape(2, 3)
  M[0, 0] = 7.7
  M[1, 0] = -1.760
  M[0, 1] = 10.05
  M[1, 1] = -1.648
  M[0, 2] = 7.7
  M[1, 2] = 1.74
  
  time_m_aux = []
  for k in range(0, 15):
    time_m_aux.append(time_m[k + 4])
  for j in range(0, 31):
    time_m_aux.append(time_m[j + 19])
  for l in range(0, 21):
    time_m_aux.append(time_m[l + 51])
  
  time_diff_abs = numpy.zeros(len(time_m))
  time_diff = numpy.zeros(len(time_m))
  for k in range(0, len(time_m)):
    time_diff_abs[k] = math.fabs((time_m[k] - time_r[k]) * 0.0000000001)
    time_diff[k] = (time_m[k] - time_r[k]) * 0.0000000001
    
  mean_for_plot_abs = numpy.zeros(len(time_m))
  variance_for_plot_abs = numpy.zeros(len(time_m))
  mean_for_plot = numpy.zeros(len(time_m))
  variance_for_plot = numpy.zeros(len(time_m))
  norm_for_plot = numpy.zeros(len(time_m))
  norm_dist = scipy.stats.norm(mean_for_plot[0], numpy.std(time_diff))
  for k in range(0, len(time_m)):
    mean_for_plot_abs[k] = numpy.mean(time_diff_abs)
    variance_for_plot_abs[k] = numpy.var(time_diff_abs)
    mean_for_plot[k] = numpy.mean(time_diff)
    variance_for_plot[k] = numpy.var(time_diff)
    norm_for_plot[k] = norm_dist.pdf(k)
  
  s1 = 'The mean of the absolute time difference is ' + "{0:.4f}".format(numpy.mean(time_diff_abs)) + ' seconds'
  s2 = 'The variance of the absolute time difference is ' + "{0:.4f}".format(numpy.var(time_diff_abs))
  print s1
  print s2
  
  print '---'
  
  s1 = 'The mean of the time difference is ' + "{0:.4f}".format(numpy.mean(time_diff)) + ' seconds'
  s2 = 'The variance of the time difference is ' + "{0:.4f}".format(numpy.var(time_diff))
  print s1
  print s2
  
  plt.subplot(2, 2, 1)
  fig = plt.gcf()
  plt.plot(x_m, y_m, '-o')
  plt.title('Positions from manual check')
  plt.ylabel('y [m]')
  plt.xlabel('x [m]')
  plt.scatter(M[0], M[1], color = 'y')
  circle1=plt.Circle((M[0, 0], M[1, 0]), 2.0, color = 'r', fill = False)
  circle2=plt.Circle((M[0, 1], M[1, 1]), 2.0, color = 'g', fill = False)
  circle3=plt.Circle((M[0, 2], M[1, 2]), 2.0, color = 'gray', fill = False)
  fig.gca().add_artist(circle1)
  fig.gca().add_artist(circle2)
  fig.gca().add_artist(circle3)
  plt.subplot(2, 2, 2)
  fig = plt.gcf()
  plt.plot(x_r, y_r, '-o')
  plt.title('Positions from robot')
  plt.ylabel('y [m]')
  plt.xlabel('x [m]')
  plt.scatter(M[0], M[1], color = 'y')
  circle1=plt.Circle((M[0, 0], M[1, 0]), 2.0, color = 'r', fill = False)
  circle2=plt.Circle((M[0, 1], M[1, 1]), 2.0, color = 'g', fill = False)
  circle3=plt.Circle((M[0, 2], M[1, 2]), 2.0, color = 'gray', fill = False)
  fig.gca().add_artist(circle1)
  fig.gca().add_artist(circle2)
  fig.gca().add_artist(circle3)
  ax_abs = plt.subplot(2, 2, 3)
  plt.plot(numpy.linspace(0, len(time_diff), len(time_diff), False), time_diff_abs)
  plt.title('Absolute time_diff')
  plt.ylabel('Abs(time_diff) [s] with the mean and variance')
  mean_plot_abs = ax_abs.plot(numpy.linspace(0, len(time_diff), len(time_diff), False), mean_for_plot_abs, label = "Mean")
  var_plot_abs = ax_abs.plot(numpy.linspace(0, len(time_diff), len(time_diff), False), variance_for_plot_abs, color = 'gray', label = "Variance")
  handles, labels = ax_abs.get_legend_handles_labels()
  plt.legend(handles[::-1], labels[::-1])
  ax = plt.subplot(2, 2, 4)
  plt.plot(numpy.linspace(0, len(time_diff), len(time_diff), False), time_diff)
  plt.title('time_diff between manual and automatic checkers')
  plt.ylabel('time_diff [s] with the mean and variance')
  mean_plot = ax.plot(numpy.linspace(0, len(time_diff), len(time_diff), False), mean_for_plot, label = "Mean")
  var_plot = ax.plot(numpy.linspace(0, len(time_diff), len(time_diff), False), variance_for_plot, color = 'gray', label = "Variance")
  handles, labels = ax.get_legend_handles_labels()
  plt.legend(handles[::-1], labels[::-1])
  plt.show()
  

if __name__ == '__main__':
  get_data_from_robot()
  get_data_from_manual_check()
  plots()
  
  
  
  