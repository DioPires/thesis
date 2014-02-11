#! /usr/bin/env python

import roslib
roslib.load_manifest('thesis')
import rospy
import math
import numpy as np
import scipy as sp
from geometry_msgs.msg import *
from std_msgs.msg import *
from std_srvs.srv import *

time_ = 0

def check_if_lost(msg):
    global time_    
    
    variance_x = msg.pose.covariance[0]
    variance_y = msg.pose.covariance[7]
    
    ellipse_of_error = variance_x * variance_y * math.pi
    
    rospy.loginfo("ellipse_of_error: %f", ellipse_of_error)
    
    if ellipse_of_error > 5.0:
        time_now = rospy.Time.now() #needed to not keeping re-localizing
        
        if math.fabs(time_now.secs - time_.secs) > 5.0:
	    print 'Robot is lost. Re-localizing...'
            time_ = time_now
            '''rospy.wait_for_service('/move_base/clear_costmaps')
            try:
                srv = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
                ans = srv()
            except rospy.ServiceException, e:
                print "Service call for clearing costmaps failed: %s" %e         
            
            rospy.wait_for_service('/global_localization')
            try:
                srv = rospy.ServiceProxy('/global_localization', Empty)
                ans = srv()
            except rospy.ServiceException, e:
                print "Service call for global localization failed: %s" %e
            '''
          

if __name__ == '__main__':
    global time_
    rospy.init_node('robot_is_lost')
    #time_ = rospy.Time()
    time_ = rospy.Time.now()
    rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, check_if_lost)
    rospy.spin()