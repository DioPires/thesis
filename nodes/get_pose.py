#! /usr/bin/env python
  
import roslib
roslib.load_manifest('thesis')
import rospy
import math
from tf import *
from geometry_msgs.msg import *
from std_msgs.msg import *


def posture_publisher(msg):
    pub = rospy.Publisher("posture", PoseStamped)

    posture = PoseStamped()
    header = Header()
    
    header = msg.header
    pose = msg.pose.pose
    
    posture = PoseStamped(header, pose)
    
    pub.publish(posture)



if __name__ == '__main__':
    rospy.init_node('posture_publisher')
    rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, posture_publisher)
    rospy.spin()
