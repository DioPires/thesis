#! /usr/bin/env python

import rospy
import roslib
import math
from sa_project.msg import ScoutMotionMsg
from sa_project.srv import ScoutMotionSrv
from geometry_msgs.msg import *
from std_srvs.srv import *
roslib.load_manifest('sa_project')

def call_global_localization_srv():
    rospy.wait_for_service('/global_localization')
    try:
	srv = rospy.ServiceProxy('/global_localization', Empty)
	ans = srv()
    except rospy.ServiceException, e:
	print "Service call for global localization failed: %s" %e




if __name__ == '__main__':
    rospy.init_node('call_global_loc_srv')
    call_global_localization_srv()
    rospy.spin()