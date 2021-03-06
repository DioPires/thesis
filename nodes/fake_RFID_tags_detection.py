#! /usr/bin/env python

import roslib
roslib.load_manifest('thesis')
roslib.load_manifest('visualization_marker_tutorials')
import rospy
import math
import numpy
from geometry_msgs.msg import *
from std_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *
from visualization_msgs.msg import *

flag_ = False
ini = 0
M_ = 0
M2_ = 0
f_tag_detection_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/RFID/tag_detection_for_manual_checking2.txt', 'a')


def define_fake_RFID_tags():
  global M_
  global M2_
  
  pub_tags = rospy.Publisher("tags_marker_array", MarkerArray)
  
  rospy.sleep(2.0)
  
  # Fake RFID tags position
  M_ = numpy.zeros(32).reshape(2, 16)
  M_[0, 0] = 4.775
  M_[1, 0] = -0.930
  M_[0, 1] = 6.374
  M_[1, 1] = 1.425
  M_[0, 2] = 8.452
  M_[1, 2] = -2.240
  M_[0, 3] = -3.446
  M_[1, 3] = -7.036
  M_[0, 4] = 13.256
  M_[1, 4] = 3.636
  M_[0, 5] = 16.733
  M_[1, 5] = -3.819
  M_[0, 6] = 15.810
  M_[1, 6] = -5.916
  M_[0, 7] = 15.793
  M_[1, 7] = -11.494
  M_[0, 8] = 16.512
  M_[1, 8] = -15.488
  M_[0, 9] = 14.480
  M_[1, 9] = -15.750
  M_[0, 10] = 12.766
  M_[1, 10] = -14.701
  M_[0, 11] = 9.907
  M_[1, 11] = -15.703
  M_[0, 12] = 7.979
  M_[1, 12] = -14.784
  M_[0, 13] = 5.611
  M_[1, 13] = -13.804
  M_[0, 14] = 7.240
  M_[1, 14] = -10.765
  M_[0, 15] = 6.287
  M_[1, 15] = -9.806
  
  M2_ = numpy.zeros(6).reshape(2, 3)
  M2_[0, 0] = 7.7
  M2_[1, 0] = -1.760
  M2_[0, 1] = 10.05
  M2_[1, 1] = -1.648
  M2_[0, 2] = 7.7
  M2_[1, 2] = 1.74
  print M2_
  
  
  # Construction of a MarkerArray for visualization purposes
  tags = MarkerArray()
  for k in range(0, len(M2_[0])):
    marker = Marker()
    marker.header.frame_id = "/map"
    #marker.id = k
    marker.type = marker.ARROW
    marker.action = marker.ADD
    marker.pose = Pose(Point(M2_[0, k], M2_[1, k], 0.0), Quaternion(0.0, 0.0, 0.0, 1.0))
    marker.scale = Vector3(1.0, 0.1, 0.2)
    marker.color = ColorRGBA(1.0, 1.0, 0.0, 1.0)
    
    tags.markers.append(marker)
    
  id = 0
  for m in tags.markers:
    m.header.seq = id
    m.header.stamp = rospy.Time.now()
    m.id = id
    m.ns = 'tags'
    id += 1
  
  pub_tags.publish(tags)
  print 'All the fake RFID tags have been set up!' 


# Check if a tag is inside the detection radius (3 meters)
def check_if_RFID_tag_is_detected(msg):
  for k in range(0, len(M2_[0])):
    d = math.sqrt((M2_[0, k] - msg.pose.position.x)**2 + (M2_[1, k] - msg.pose.position.y)**2)
    if d <= 2.0:
      #if "True" in flag_:
      s = 'Tag ' + str(k) + ' detected!\n' + str(rospy.Time.now()) + '\n' + str(msg.pose) + '\n---\n'
      f_tag_detection_.seek(0, 2)
      f_tag_detection_.write(s)
      print s

      
def write2files(msg):
  global flag_
  flag_ = str(msg)
  
  if "Shutdown" in flag_:
    f_tag_detection_.close()
    rospy.signal_shutdown('Tag detection node stopped!')
      
      
def ini_pose_getter(msg, pub):
  global ini
  if ini <= 10:
    pub.publish(msg)
    ini += 1
      
      
if __name__ == '__main__':
  rospy.init_node('fake_RFID_tags_detection_node')
  pub_ini_pose = rospy.Publisher('/initialpose', PoseWithCovarianceStamped)
  
  rospy.sleep(2.0)
  
  define_fake_RFID_tags()
  
  msg = PoseWithCovarianceStamped()
  msg.header.frame_id = 'map'
  msg.pose.pose.position.x = 0.75
  msg.pose.pose.position.y = -0.25
  #msg.pose.pose.position.x = 0.0
  #msg.pose.pose.position.y =0.0
  msg.pose.pose.orientation.x = 0
  msg.pose.pose.orientation.y = 0
  msg.pose.pose.orientation.z = 0
  msg.pose.pose.orientation.w = 1
  msg.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]
  
  pub_ini_pose.publish(msg)
  rospy.Subscriber('/posture', PoseStamped, check_if_RFID_tag_is_detected)
  rospy.Subscriber('/write_to_files', String, write2files)
  rospy.spin()
  