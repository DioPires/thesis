#! /usr/bin/env python

from geometry_msgs.msg import *
import rospy
from std_msgs.msg import *


def publish_pose(pub):
  pose = geometry_msgs.msg.PoseStamped()
  
  while not rospy.is_shutdown():
    pose.pose.position = Point(-1.5, 1.5, 2)
    pose.pose.orientation = Quaternion(0, 0, 0, 1)
    pub.publish(pose)

  
if __name__ == '__main__':
  rospy.init_node('publish_pose')
  pub = rospy.Publisher('/pose_published', geometry_msgs.msg.PoseStamped)
  publish_pose(pub)
  rospy.spin()