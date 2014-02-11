#! /usr/bin/env python

import rospy
import roslib
import math
from sa_project.msg import ScoutMotionMsg
from sa_project.srv import ScoutMotionSrv
from geometry_msgs.msg import *
roslib.load_manifest('sa_project')


def publish_vel(msg):
    enable = True
    velocity_left = int(math.ceil((msg.linear.x - 0.36 * msg.angular.z / 2) * 23.0)) * -100
    vel_right = int(math.ceil((msg.linear.x + 0.36 * msg.angular.z / 2) * 23.0)) * 100

    velocity_right = compensate_error(vel_right)
    #velocity_right = vel_right
    
    print('velocity_left: ', velocity_left)
    print('vel_right: ', vel_right)
    print('velocity_right: ', velocity_right)

    rospy.wait_for_service('/scout/motion')
    try:
	srv = rospy.ServiceProxy('/scout/motion', ScoutMotionSrv)
	ans = srv(enable, velocity_left, velocity_right)
    except rospy.ServiceException, e:
	print "Service call for scout motion failed: %s" %e


def compensate_error(vel_right):
    sign = math.copysign(1, vel_right)
    
    vel = abs(vel_right)
    if (vel >= 400):
	error = 0.01 * vel
    else:
	error = 1 / 300.0 * vel + 8 / 3.0
	
    new_vel = int(math.ceil(vel + error) * sign)
    
    if (vel_right == 0):
	new_vel = 0
	
    return new_vel


if __name__ == '__main__':
    rospy.init_node('send_vel')
    rospy.Subscriber('/cmd_vel', Twist, publish_vel)
    rospy.spin()
