#! /usr/bin/env python

import rospy
from geometry_msgs.msg import *
from std_msgs.msg import *


def cast_to_string(msg):
  f = open('/home/diogopires/Desktop/test.txt', 'w')
  
  i = 1
  while i <= 50:
    s = str(msg)
    f.write(s)
    i = i + 1
  f.close()
  rospy.signal_shutdown('')
  
  
if __name__ == '__main__':
  rospy.init_node('cast_to_string_node')
  rospy.Subscriber('/pose_published', PoseStamped, cast_to_string)
  rospy.spin()