#!/usr/bin/env python
#include <sensor_msgs/Joy.h>
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy

def callback(data):
    #Buttons
    if data.buttons[0] == 1:
        rospy.loginfo("Button: A")
    if data.buttons[1] == 1:
        rospy.loginfo("Button: B")
    if data.buttons[2] == 1:
        rospy.loginfo("Button: X")
    if data.buttons[3] == 1:
        rospy.loginfo("Button: Y")
    if data.buttons[4] == 1:
        rospy.loginfo("Button: LB")
    if data.buttons[5] == 1:
        rospy.loginfo("Button: RB")
    if data.buttons[6] == 1:
        rospy.loginfo("Button: CHANGE VIEW")
    if data.buttons[7] == 1:
        rospy.loginfo("Button: MENU")
    if data.buttons[8] == 1:
        rospy.loginfo("Button: HOME")
    if data.buttons[9] == 1:
        rospy.loginfo("Button: LEFT JOYSTICK PUSH")
    if data.buttons[10] == 1:
        rospy.loginfo("Button: RIGHT JOYSTICK PUSH")
    #AXES
        #LEFT
    if data.axes[0] == 1:
        rospy.loginfo("AXES:  LEFT JOYSTICK:LEFT")
    if data.axes[0] == -1:
        rospy.loginfo("AXES:  LEFT JOYSTICK:RIGHT")
    if data.axes[1] == 1:
        rospy.loginfo("AXES:  LEFT JOYSTICK:UP")
    if data.axes[1] == -1:
        rospy.loginfo("AXES:  LEFT JOYSTICK:DOWN")
    if data.axes[2] == -1:
        rospy.loginfo("AXES:  LEFT TRIGERS:DOWN")
        #RIGHT
    if data.axes[3] == 1:
        rospy.loginfo("AXES:  RIGHT JOYSTICK:LEFT")
    if data.axes[3] == -1:
        rospy.loginfo("AXES:  RIGHT JOYSTICK:RIGHT")
    if data.axes[4] == 1:
        rospy.loginfo("AXES:  RIGHT JOYSTICK:UP")
    if data.axes[4] == -1:
        rospy.loginfo("AXES:  RIGHT JOYSTICK:DOWN")
    if data.axes[5] == -1:
        rospy.loginfo("AXES:  RIGHT TRIGERS:DOWN")
    

        #DIRECTIONAL PAD
    if data.axes[6] == 1:
        rospy.loginfo("AXES:  DIRECTIONAL PAD:LEFT")
    if data.axes[6] == -1:
        rospy.loginfo("AXES:  DIRECTIONAL PAD:RIGHT")
    if data.axes[7] == -1:
        rospy.loginfo("AXES:  DIRECTIONAL PAD:DOWN")
    if data.axes[7] == 1:
        rospy.loginfo("AXES:  DIRECTIONAL PAD:UP")
    
def joyListener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('joyListenerNode', anonymous=True)

    rospy.Subscriber("joy", Joy, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    joyListener()