#! /usr/bin/env python

import roslib
roslib.load_manifest('cortex')
import rospy
import math
from cortex.msg import *
from std_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *


robot_ = Point(0.0, 0.0, 0.0)
goal_  = Point(1.0, 1.0, 0.0)
default_ = Point(-3.361, 3.605, -math.pi / 2.0)

kinect_msg = []
katana_msg = []

time_ = 0.0

ant_true_ = []
ant_false_ = []
ant_P2_ = False
ant_P7_ = False
ant_P8_ = False

def publisher():
    pub = rospy.Publisher("/predicates", Predicates)

    global robot_
    global default_
    global goal_
    global time_
    global ant_true_
    global ant_false_
    global ant_P2_
    global ant_P7_
    global ant_P8_
    
    true_predicates = []
    false_predicates = []
   
    P1 = "ConnectionLost"
    P2 = 'Request'
    P3 = 'IsAtReqPos'        
    P4 = 'IsAtDefaultPos'
    P5 = 'IsArmStopped'
    P6 = 'IsArmAtDefault'
    P7 = 'ShouldITeleop'  
    P8 = 'ShouldIMoveArm'        
    
    now = rospy.get_time()
    
    print "Robot:"
    print robot_
    print "Goal:"
    print goal_
    print "\n"

    if( abs(now - time_) > 1000.0):
        true_predicates.append(P1)
        false_predicates.append(P2)
        false_predicates.append(P7)
        false_predicates.append(P8)
        ant_P2_ = False
        ant_P7_ = False
        ant_P8_ = False
    elif ('Teleoperation mode' in str(kinect_msg) or \
          'Move back' in str(kinect_msg) or \
          'Move front' in str(kinect_msg) or \
          'Turn right' in str(kinect_msg) or \
          'Turn left' in str(kinect_msg) or \
          'Teop Stop' in str(kinect_msg)):
        true_predicates.append(P7)
        false_predicates.append(P1)
        false_predicates.append(P2)
        false_predicates.append(P8)
        ant_P2_ = False
        ant_P7_ = True
        ant_P8_ = False
    elif ('Exit teleoperation mode' in str(kinect_msg) or \
          'Stop' in str(kinect_msg)):
        false_predicates.append(P1)
        false_predicates.append(P2)
        false_predicates.append(P7)
        false_predicates.append(P8)
        ant_P2_ = False
        ant_P7_ = False
        ant_P8_ = False
    elif ('Returning to base' in str(kinect_msg)):
        true_predicates.append(P2)
        false_predicates.append(P1)
        false_predicates.append(P7)
        false_predicates.append(P8)
        ant_P2_ = True
        ant_P7_ = False
        ant_P8_ = False
    elif ('Coming to help' in str(kinect_msg) or \
          'Corner1' in str(kinect_msg) or \
          'Corner2' in str(kinect_msg)):
        true_predicates.append(P2)
        true_predicates.append(P8)
        false_predicates.append(P1)
        false_predicates.append(P7)
        ant_P2_ = True
        ant_P7_ = False
        ant_P8_ = True
    else:
        false_predicates.append(P1)
        if ant_P2_:
            true_predicates.append(P2)
        else:
            false_predicates.append(P2)
        if ant_P7_:
            true_predicates.append(P7)
        else:
            false_predicates.append(P7)
        if ant_P8_:
            true_predicates.append(P8)
        else:            
            false_predicates.append(P8)

    if (abs(robot_.x - goal_.x) < 0.2 and \
        abs(robot_.y - goal_.y) < 0.2):
       true_predicates.append(P3)
    else:
       false_predicates.append(P3)        
    
    if (abs(robot_.x - default_.x) < 2 and \
        abs(robot_.y - default_.y) < 2):
       true_predicates.append(P4)
    else:
       false_predicates.append(P4)
       
    if (katana_msg == 'Helping' or \
        katana_msg == 'Handing' or \
        katana_msg == 'Grasping'):
        true_predicates.append(P5)
    else:
        false_predicates.append(P5)
       
    if (katana_msg == 'Returning to default'):
        true_predicates.append(P6)
    else:
        false_predicates.append(P6)
    
    if ant_true_ != true_predicates and \
       ant_false_ != false_predicates:
        ant_true_  = true_predicates
        ant_false_ = false_predicates
        pr = Predicates(true_predicates,false_predicates)
        pub.publish(pr)

def posesub(msg):
       
    global robot_
    robot_.x = msg.pose.position.x
    robot_.y = msg.pose.position.y
    
    #qt = Quaternion([str(msg.pose.orientation.x), str(msg.pose.orientation.y), str(msg.pose.orientation.z), str(msg.pose.orientation.w)])
    
    #euler = euler_from_quaternion(msg.pose.orientation)
    
    #robot_.z = euler[2]
    
def goalsub(msg):
       
    global goal_
    goal_.x = msg.pose.position.x
    goal_.y = msg.pose.position.y
    
    #qt = Quaternion([str(msg.pose.orientation.x), str(msg.pose.orientation.y), str(msg.pose.orientation.z), str(msg.pose.orientation.w)])
    
    #euler = euler_from_quaternion(msg.pose.orientation)
    
    #goal_.z = euler[2]
    
def decodekinect(msg):
    
    global kinect_msg
    global time_
    
    kinect_msg = String(msg)
    time_ = rospy.get_time()

    #print kinect_msg
def decodekatana(msg):
    
    global katana_msg
    
    katana_msg = String(msg)    
    

if __name__ == '__main__':
    rospy.init_node('predicates_pub')

    global katana_msg
    global kinect_msg    
    
    katana_msg = []
    kinect_msg = []

    rospy.Subscriber('/kinect_actions', String, decodekinect)
    rospy.Subscriber('/katana_actions', String, decodekatana)    
    rospy.Subscriber('/posture', PoseStamped, posesub)
    rospy.Subscriber('/move_base_simple/goal', PoseStamped, goalsub)
    while not rospy.is_shutdown():
        publisher()

    rospy.spin()