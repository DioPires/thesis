#! /usr/bin/env python

import rospy
import roslib
import math
from geometry_msgs.msg import *
from std_srvs.srv import *
roslib.load_manifest('thesis')
import time

toc = 0.0

def call_global_localization_srv():
  rospy.wait_for_service('/global_localization')
  try:
    srv = rospy.ServiceProxy('/global_localization', Empty)
    ans = srv()
    tic = time.time()
  except rospy.ServiceException, e:
    print "Service call for global localization failed: %s" %e
  
  if toc != 0.0:
    print 'Time elapsed: %s' % str(toc - tic)


def check_if_localized(msg):
  global toc
  variance_x = msg.pose.covariance[0]
  variance_y = msg.pose.covariance[7]
    
  ellipse_of_error = variance_x * variance_y * math.pi
  print ellipse_of_error
  if ellipse_of_error <= 1.5:
    toc = time.time()

  
if __name__ == '__main__':
  rospy.init_node('call_global_loc_srv')
  rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, check_if_localized)
  call_global_localization_srv()
  rospy.spin()