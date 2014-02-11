#! /usr/bin/env python

import roslib
import rospy
import tf
from sa_project.msg import ScoutMotorsMsg
import math
roslib.load_manifest('sa_project')


#IinitRencoder = 0
#InitLencoder = 0
#InitFlag=0;

LapLeftEnc = 47824
LapRightEnc = 47481
LapDist = 0.634

LastRightEnc = 0
LastLeftEnc = 0
flag = 0

#variaveis que armazenam o total da odom
xodom = 0
yodom = 0
todom = 0

def EncodeTf(msg):
    global LapRightEnc, LapLeftEnc, LapDist, LastRightEnc, LastLeftEnc, flag, xodom, yodom, todom

    if (flag == 0):
        LastRightEnc = msg.count_right
        LastLeftEnc = msg.count_left
        flag = 1
    else:
        DLeftEnc = LastLeftEnc - msg.count_left
        DRightEnc = msg.count_right - LastRightEnc
        
        DLeft = (LapDist / LapLeftEnc) * DLeftEnc
        DRight = LapDist / LapRightEnc * DRightEnc
        
        theta = (DRight - DLeft) / 0.36 #Wheel axis distance=36cm
        todom = todom + theta
        x = (DRight + DLeft) / 2 * math.cos(todom)
        y = (DRight + DLeft) / 2 * math.sin(todom)
        xodom = xodom + x
        yodom = yodom + y
        
        LastRightEnc = msg.count_right
        LastLeftEnc = msg.count_left
        
        br = tf.TransformBroadcaster()
        br.sendTransform((xodom, yodom, 0.175),
                         tf.transformations.quaternion_from_euler(0, 0, todom),
                         rospy.Time.now(),
                         "base_link",
                         "odom")
        
if __name__ == '__main__':
    rospy.init_node('Encoder2TF')    
    rospy.Subscriber('scout/motors', ScoutMotorsMsg, EncodeTf)
    rospy.spin()
