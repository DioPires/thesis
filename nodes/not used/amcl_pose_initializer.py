#! /usr/bin/env python

import rospy
import tf
from geometry_msgs.msg import *
import roslib
roslib.load_manifest('sa_project')


def PoseWithCovarianceStamped_publisher(msg):
    pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped)
    
    """
    new_pose.header.seq = msg.header.seq
    new_pose.header.stamp = msg.header.stamp
    new_pose.header.frame_id = msg.header.frame_id

    new_pose.pose.covariance = msg.pose.covariance

    new_pose.pose.pose.position.x = msg.pose.pose.position.x
    new_pose.pose.pose.position.y = msg.pose.pose.position.y
    new_pose.pose.pose.position.z = msg.pose.pose.position.z

    new_pose.pose.pose.orientation.x = msg.pose.pose.orientation.x
    new_pose.pose.pose.orientation.y = msg.pose.pose.orientation.y
    new_pose.pose.pose.orientation.z = msg.pose.pose.orientation.z
    new_pose.pose.pose.orientation.w = msg.pose.pose.orientation.w

    pub.publish(PoseWithCovarianceStamped(new_pose))
    """

    pub.publish(msg)
    rospy.sleep(4.0)

if __name__ == '__main__':
    rospy.init_node('amcl_pose_initializer')
    rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, PoseWithCovarianceStamped_publisher)
    rospy.spin()
