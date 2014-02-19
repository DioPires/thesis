#! /usr/bin/env python

import roslib
roslib.load_manifest('thesis')
import rospy
import math
from geometry_msgs.msg import *
from std_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *
import actionlib
import move_base_msgs.msg
#import sound_play.msg


posture1_ = Pose(Point(6.646, -12.235, 0.000), Quaternion(0.000, 0.000, 0.000, 1.510))
posture2_ = Pose(Point(0.711, 0.113, 0.000), Quaternion(0.000, 0.000, 0.000, -3.124))
frame_id_ = '/map'

#speech_ = sound_play.msg.SoundRequest()

f_amcl_pose_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/amcl_pose.txt', 'r+a')
f_particlecloud_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/particlecloud.txt', 'r+a')
f_scan_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/scan.txt', 'a')
f_pose_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/pose.txt', 'a')
f_cmd_vel_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/cmd_vel.txt', 'a')
f_path_ = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/path.txt', 'a')


def send_positions():
    global posture1_
    global posture2_
    global frame_id_

    pub = rospy.Publisher("goal_posture", PoseStamped)
    #pub_speech = rospy.Publisher("robotsound", sound_play.msg.SoundRequest)
    pub_flag_write2files = rospy.Publisher("write_to_files", String)
    
    client = actionlib.SimpleActionClient("move_base", move_base_msgs.msg.MoveBaseAction)
    client.wait_for_server()
    
    posture_stamped = PoseStamped()
    posture_stamped.header.frame_id = frame_id_
    
    states = ['PENDING', 'ACTIVE', 'PREEMPTED', 'SUCCEEDED', 'ABORTED', 'REJECTED', 'PREEMPTING', 'RECALLING', 'RECALLED', 'LOST']
    f_action_result = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/mctests_action_results.txt', 'r')
    
    for line in f_action_result:
      if "Test" in line:
	if line[6].isdigit():
	  n_str = line[5] + line[6]
	  n = int(n_str)
	else:
	  n = int(line[5])

    f_action_result.close()
    f_action_result = open('/home/diogopires/ros_workspace/catkin_ws/src/thesis/test_result_files/navigation/mctests_action_results.txt', 'a')
    
    i = n + 1
    seq = 0
    while True: 
      posture_stamped.header.seq = seq
      posture_stamped.header.stamp = rospy.Time.now()
      posture_stamped.pose = posture1_
      goal = move_base_msgs.msg.MoveBaseGoal(posture_stamped)
      
      print 'Going to the elevator...'
      #speech_publish(pub_speech, 'Going to the elevator')
      f_amcl_pose_.seek(0, 2)
      f_amcl_pose_.write('\n-------- Test ' + str(i) + ' --------\n')
      f_amcl_pose_.seek(0, 2)
      f_amcl_pose_.write('=== To the elevator === \n')
      f_particlecloud_.seek(0, 2)
      f_particlecloud_.write('\n-------- Test ' + str(i) + ' --------\n')
      f_particlecloud_.seek(0, 2)
      f_particlecloud_.write('=== To the elevator === \n')
      f_scan_.seek(0, 2)
      f_scan_.write('\n-------- Test ' + str(i) + ' --------\n')
      f_scan_.seek(0, 2)
      f_scan_.write('=== To the elevator === \n')
      f_pose_.seek(0, 2)
      f_pose_.write('\n-------- Test ' + str(i) + ' --------\n')
      f_pose_.seek(0, 2)
      f_pose_.write('=== To the elevator === \n')
      f_cmd_vel_.seek(0, 2)
      f_cmd_vel_.write('\n-------- Test ' + str(i) + ' --------\n')
      f_cmd_vel_.seek(0, 2)
      f_cmd_vel_.write('=== To the elevator === \n')
      f_path_.seek(0, 2)
      f_path_.write('\n-------- Test ' + str(i) + ' --------\n')
      f_path_.seek(0, 2)
      f_path_.write('=== To the elevator === \n')
      
      pub.publish(posture_stamped)
      client.send_goal(goal)
      pub_flag_write2files.publish(String("True"))
      client.wait_for_result()
      pub_flag_write2files.publish(String("False"))
      
      s = '\nTest ' + str(i) + ' -> going to the elevator: ' + states[client.get_state()] + '\n'
      f_action_result.write(s)
      print s
      #speech_publish(pub_speech, 'I am at the elevator')
      
      posture_stamped.header.seq = seq + 1
      posture_stamped.header.stamp = rospy.Time.now()
      posture_stamped.pose = posture2_
      goal = move_base_msgs.msg.MoveBaseGoal(posture_stamped)
      
      print 'Going to LRM...'
      #speech_publish(pub_speech, 'Going to LRM')
      f_amcl_pose_.seek(0, 2)
      f_amcl_pose_.write('=== To the LRM === \n')
      f_particlecloud_.seek(0, 2)
      f_particlecloud_.write('=== To the LRM === \n')
      f_scan_.seek(0, 2)
      f_scan_.write('=== To the LRM === \n')
      f_pose_.seek(0, 2)
      f_pose_.write('=== To the LRM === \n')
      f_cmd_vel_.seek(0, 2)
      f_cmd_vel_.write('=== To the LRM === \n')
      f_path_.seek(0, 2)
      f_path_.write('=== To the LRM === \n')
      
      pub.publish(posture_stamped)
      client.send_goal(goal)
      pub_flag_write2files.publish(String("True"))
      client.wait_for_result()
      pub_flag_write2files.publish(String("False"))
      
      s = 'Test ' + str(i) + ' -> going to LRM: ' + states[client.get_state()] + '\n\n'
      f_action_result.write(s)
      print s
      #speech_publish(pub_speech, 'I am at LRM')
      
      i = i + 1
      seq = seq + 2
            
      data = raw_input('Do you want to go for another round? (y / n)\n')
      if data == 'y':
	  print 'Lets go then!'
      else:
	  data = raw_input('Do you want to stop? (y / n)\n')
	  if data == 'y':
	      break
	  else:
	      raw_input('Press enter when you do...')
	      
    f_action_result.close()
    f_amcl_pose_.close()
    f_particlecloud_.close()
    f_scan_.close()
    f_pose_.close()
    f_cmd_vel_.close()
    f_path_.close()
    pub_flag_write2files.publish(String("Shutdown"))
    rospy.signal_shutdown('Ending Monte-Carlo tests...')
    

'''def speech_publish(pub_speech, msg):
    global speech_
    
    speech_.sound = -3
    speech_.command = 1
    speech_.arg = msg
    
    pub_speech.publish(speech_)
'''

if __name__ == '__main__':
    rospy.init_node('send_positions_for_monte_carlo_test')
    send_positions()
    rospy.spin()
    