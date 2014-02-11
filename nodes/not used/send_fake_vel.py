#! /usr/bin/env python

import rospy
import roslib
from geometry_msgs.msg import *
roslib.load_manifest('sa_project')


def publish_vel_twist():
    pub = rospy.Publisher('/cmd_vel', Twist)

    vel = Twist()
  
    vel.linear.x = 0.0
    vel.linear.y = 0.0
    vel.linear.z = 0.0
    vel.angular.x = 0.0
    vel.angular.y = 0.0
    vel.angular.z = 0.5
    
    while not rospy.is_shutdown():
	pub.publish(vel)



if __name__ == '__main__':
    rospy.init_node('cmd_vel')
    publish_vel_twist()
    rospy.spin()