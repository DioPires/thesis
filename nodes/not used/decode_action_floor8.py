#! /usr/bin/env python
  
import roslib
roslib.load_manifest('cortex')
roslib.load_manifest('sa_project')
import rospy
import math
from geometry_msgs.msg import *
from std_msgs.msg import *
from cortex.msg import *
from sa_project.srv import ScoutMotionSrv


posture_ = PoseStamped()
posture_to_stop_ = PoseStamped()
kinect_action_msg_ = String()
id_ = 1 #for header.seq

def decode_action(msg):
     global id_
     global kinect_action_msg_
     global posture_
     global posture_to_stop_
     
     pub = rospy.Publisher('move_base_simple/goal', PoseStamped)
     #pub_actions = rospy.Publisher('/actions_for_katana', String)
     
     #pub_actions.publish(String(msg))
     
     #print msg
     
     if ('MoveDefault' in str(msg)):
         print 'Go to default'
	
         #pub = rospy.Publisher('move_base_simple/goal', PoseStamped)
   
         posture = PoseStamped()
         header = Header()
         pose = Pose()
         point = Point()
         orientation = Quaternion()
	
         header.seq = id_
         header.stamp = rospy.Time.now()
         header.frame_id = '/map'
	
         point.x = 1.182
         point.y = -0.003
         point.z = 0.000
	
         orientation.x = 0.000
         orientation.y = 0.000
         orientation.z = 0.038
         orientation.w = 0.999
	
         pose = Pose(point, orientation)
	
         posture = PoseStamped(header, pose)
	
         pub.publish(posture)
	
         id_ = id_ + 1
         msg = []
     elif ('Stop' in str(msg)):
         print 'Stopping'
         print str(msg)
         
         posture_to_stop_.header.seq = id_
         posture_to_stop_.header.stamp = rospy.Time.now()
         posture_to_stop_.header.frame_id = '/map'

         pub.publish(posture_to_stop_)

         id_ = id_ + 1

         msg = []
     elif ('MoveToReqPos' in str(msg)):
         print 'MoveToReqPos'
	
         #pub = rospy.Publisher('move_base_simple/goal', PoseStamped)
	
         posture_.header.seq = id_
         posture_.header.stamp = rospy.Time.now()
         posture_to_stop_.header.frame_id = '/map'
	
         id_ = id_ + 1
	
         print posture_
         pub.publish(posture_)
         msg = []
     elif ('Teleop' in str(msg)):
         print 'Teleop mode'
         enable = True
         linear_vel = 0.0
         angular_vel = 0.0
         while ('Exit teleoperation mode' not in str(kinect_action_msg_)):    
             if ('Move back' in str(kinect_action_msg_)):
                 print 'Move back'
                 linear_vel = -0.1
                 angular_vel = 0.0
             elif ('Move front' in str(kinect_action_msg_)):
                 print 'Move front'
                 linear_vel = 0.1
                 angular_vel = 0.0
             elif ('Turn right' in str(kinect_action_msg_)):
                 print 'Turn right'
                 linear_vel = 0.0
                 angular_vel = math.pi / 4
             elif ('Turn left' in str(kinect_action_msg_)): 
                 print 'Turn left'
                 linear_vel = 0.0
                 angular_vel = -math.pi / 4
             elif ('Teop Stop' in str(kinect_action_msg_)):
                 print 'Teop Stop'
                 linear_vel = 0.0
                 angular_vel = 0.0
	    
             velocity_left = int(math.ceil((linear_vel - 0.36 * angular_vel / 2) * 23.0)) * -100
             vel_right = int(math.ceil((linear_vel + 0.36 * angular_vel / 2) * 23.0)) * 100

             velocity_right = compensate_error(vel_right)

             rospy.wait_for_service('/scout/motion')
             try:
                srv = rospy.ServiceProxy('/scout/motion', ScoutMotionSrv)
                ans = srv(enable, velocity_left, velocity_right)
             except rospy.ServiceException, e:
                print "Service call for scout motion failed: %s" %e
	
         velocity_left = int(math.ceil((linear_vel - 0.36 * angular_vel / 2) * 23.0)) * -100
         vel_right = int(math.ceil((linear_vel + 0.36 * angular_vel / 2) * 23.0)) * 100

         velocity_right = compensate_error(vel_right)

         rospy.wait_for_service('/scout/motion')
         try:
             srv = rospy.ServiceProxy('/scout/motion', ScoutMotionSrv)
             ans = srv(enable, velocity_left, velocity_right)
         except rospy.ServiceException, e:
             print "Service call for scout motion failed: %s" %e
	
     
def update_stop_posture(msg):
    #print 'Entrei no stop'
    #global id_
    
    posture_to_stop_ = msg
    """ 
    msg.header.seq = id_
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = '/map'

    pub.publish(msg)

    id_ = id_ + 1
    """

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
    

def decode_kinect_action(msg):
    global posture_
    global kinect_action_msg_
    
    header = Header()
    pose = Pose()
    point = Point()
    orientation = Quaternion()
    
    kinect_action_msg_ = String(msg)
    
    if ('Returning to base' in str(msg)):
	header.seq = 0
	header.stamp = rospy.Time()
	header.frame_id = '/map'
	
	point.x = 1.182
	point.y = -0.003
	point.z = 0.000
	
	orientation.x = 0.000
	orientation.y = 0.000
	orientation.z = 0.038
	orientation.w = 0.999
 
	pose = Pose(point, orientation)
	
	posture_ = PoseStamped(header, pose)
    elif ('Coming to help' in str(msg)):
	header.seq = 0
	header.stamp = rospy.Time()
	header.frame_id = '/map'
	
	point.x = 7.164
	point.y = -11.060
	point.z = 0.000
	
	orientation.x = 0.000
	orientation.y = 0.000
	orientation.z = -0.093
	orientation.w = 0.996
 
	pose = Pose(point, orientation)
	
	posture_ = PoseStamped(header, pose)
    elif ('Corner1' in str(msg)):
	header.seq = 0
	header.stamp = rospy.Time()
	header.frame_id = '/map'
	
	point.x = 8.011
	point.y = -0.623
	point.z = 0.000
	
	orientation.x = 0.000
	orientation.y = 0.000
	orientation.z = 0.216
	orientation.w = 0.976
	
	pose = Pose(point, orientation)
	
	posture_ = PoseStamped(header, pose)
    elif ('Corner2' in str(msg)):
	header.seq = 0
	header.stamp = rospy.Time()
	header.frame_id = '/map'
	
	point.x = 12.765
	point.y = 1.400
	point.z = 0.000
	
	orientation.x = 0.000
	orientation.y = 0.000
	orientation.z = -0.295
	orientation.w = 0.956
 
	pose = Pose(point, orientation)
	
	posture_ = PoseStamped(header, pose)
	
	
if __name__ == '__main__':
    rospy.init_node('decode_actions')
    rospy.Subscriber('/actions', Actions, decode_action)
    rospy.Subscriber('/kinect_actions', String, decode_kinect_action)
    rospy.Subscriber('/posture', PoseStamped, update_stop_posture)
    rospy.spin()
    