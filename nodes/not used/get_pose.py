#! /usr/bin/env python
  
import roslib
roslib.load_manifest('sa_project')
import rospy
import math
import tf
from geometry_msgs.msg import *
from std_msgs.msg import *


def odom2base_transform():
    listener = tf.TransformListener()
    broadcaster = tf.TransformBroadcaster()
    
    pub = rospy.Publisher("pose", PoseStamped)

    counter = 0
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform('base_link', 'map', rospy.Time.now())
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        posture = PoseStamped()
        header = Header()
        pose = Pose()
        point = Point()
        orientation = Quaternion()
        
        header.seq = counter + 1
        header.stamp = rospy.Time.now()
        header.frame_id = '/base_link'
        
        point.x = trans[0]
        point.y = trans[1]
        point.z = trans[2] + 0.175

        orientation.x = rot[0]
        orientation.y = rot[1]
        orientation.z = rot[2]
        orientation.w = rot[3]

        pose.position = Point(point.x, point.y, point.z)
        pose.orientation = Quaternion(orientation.x, orientation.y, orientation.z, orientation.w)

        posture = PoseStamped(header, pose)
        
        pub.publish(posture)
        
        counter = counter + 1



if __name__ == '__main__':
    rospy.init_node('odom2base_node')
    odom2base_transform()
    rospy.spin()
