#! /usr/bin/env python

import roslib
roslib.load_manifest('thesis')
import rospy
import math
import numpy
from geometry_msgs.msg import *
from std_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *


pose_ = PoseStamped()
flag_ = False
tag_ = 0
f_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/RFID/manual_tag_detection2.txt', 'a')


def manual_checking():
  global flag_
  global tag_
  
  isInTag = False
  while not rospy.is_shutdown():
    data = raw_input('\nPress 1, 2, 3 or q\n')
    if "1" in data:
      isInTag = True
      while isInTag:
	flag_ = True
	tag_ = 0
	#write_in_file(0)
	exit_data = raw_input("\nPress '1' to exit tag 1\n")
	if "1" in exit_data:
	  isInTag = False
	  flag_ = False
	  break
	else:
	  print "\nYou need to press '1' to exit this tag!\n"
    elif "2" in data:
      isInTag = True
      while isInTag:
	flag_ = True
	tag_ = 1
	#write_in_file(1)
	exit_data = raw_input("\nPress '2' to exit tag 2\n")
	if "2" in exit_data:
	  isInTag = False
	  flag_ = False
	  break
	else:
	  print "\nYou need to press '2' to exit this tag!\n"
    elif "3" in data:
      isInTag = True
      while isInTag:
	flag_ = True
	tag_ = 2
	#write_in_file(2)
	exit_data = raw_input("\nPress '3' to exit tag 3\n")
	if "3" in exit_data:
	  isInTag = False
	  flag_ = False
	  break
	else:
	  print "\nYou need to press '3' to exit this tag!\n"
    elif "q" in data:
      f_.close()
      rospy.signal_shutdown('Shutting down...')
    else:
      print "Acceptable inputs are '1', '2' and '3' for tags 1, 2 and 3, respectively, and 'q' for shutting down"


def write_in_file(tag):
  while flag_:
    s = str(tag) + '\n' + str(rospy.Time.now()) + '\n' + str(pose_) + '\n---\n'
    f_.write(s)
      
      
def save_posture(msg):
  #global pose_
  #pose_ = msg.pose
  if flag_:
    s = str(tag_) + '\n' + str(rospy.Time.now()) + '\n' + str(msg.pose) + '\n---\n'
    f_.write(s)
      
      
if __name__ == '__main__':
  #global pose_
  
  rospy.init_node('fake_RFID_tags_detection_checker_node')
  #pose_ = Pose()
  rospy.Subscriber('/posture', PoseStamped, save_posture)
  manual_checking()
  rospy.spin()