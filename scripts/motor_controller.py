#!/usr/bin/env python
""" This program receives the String from the keyboard_teleop.py and sends a message to control
    the ros_simple_dc_motor.ino.
    If the pressed key is:
        i --> Motor full speed to the front  (vel=255)
        l --> Motor Stop (vel=0)
        , --> Motor full speed reverse (vel=-255)
    Subscribed Topics:
        /pressed_key
    Published Topics:
        /arduino/motor_vel
"""
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String

#### GLOBAL VARIABLES ####
motor_vel = Int32() #Motor velocity Int32 ROS message


def pressed_key_cb(key_msg):
    global motor_vel
    max_speed = 255 #Maximum speed: you could change the maximum possible value from 0 to 255
    velocity_value={'i':max_speed,'k':0,',':-1*max_speed}
    #This function is executed when a new message arrives to the pressed key topic
    if key_msg.data in velocity_value.keys():
        motor_vel.data=velocity_value[key_msg.data]
    else:
        print("Not valid key was pressed. Motor will stop")
        motor_vel.data=0
    print(motor_vel)

def MotorController():
    #########Init the node ################
    rospy.init_node("motor_controller", anonymous=True)
    print("Node initialized")
    ############ CONSTANTS ################
    global motor_vel
    ####    PUBLISHERS    ####
    print("Setting publishers...")
    pub_motor_vel = rospy.Publisher('arduino/motor_vel', Int32, queue_size=1)
    print("Publishers ok")
    print("Starting Node...")

    ####    SUBSCRIBERS    ####
    rospy.Subscriber("pressed_key", String, pressed_key_cb)
    r = rospy.Rate(10) #rate in Hz
    
    while not rospy.is_shutdown():
        pub_motor_vel.publish(motor_vel) #publish the number
        r.sleep()




############################### MAIN PROGRAM ####################################

if __name__ == "__main__":
    try:
        MotorController()
    except:
        rospy.logfatal("motor_controller died")
