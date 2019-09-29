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


class MotorController():
    def __init__(self):
        ############ CONSTANTS ################
        self.max_speed = 255 #Maximum speed you could change the maximum possible valu from 0 to 255
        self.velocity_value={'i':self.max_speed,'k':0,',':self.max_speed*-1}
        print self.velocity_value
        self.motor_vel = Int32() #Motor velocity ROS message
        ###******* INIT PUBLISHERS *******###
        print("Setting publishers...")
        ##  pub = rospy.Publisher('setPoint', UInt16MultiArray, queue_size=1)
        self.pub_motor_vel = rospy.Publisher('arduino/motor_vel', Int32, queue_size=1)
        print("Publishers ok")
        print("Starting Node...")

        ############################### SUBSCRIBERS #####################################
        rospy.Subscriber("pressed_key", String, self.pressed_key_cb)
        rospy.on_shutdown(self.cleanup) #This function will be executed before the node dies


        r = rospy.Rate(10) #rate in Hz
        print("Node initialized")

        while not rospy.is_shutdown():
            self.pub_motor_vel.publish(self.motor_vel) #publish the number
            r.sleep()

    def pressed_key_cb(self, key):
        #This function is executed when a new message arrives to the pressed key topic
        if key.data in self.velocity_value.keys():
            self.motor_vel.data=self.velocity_value[key.data]
        else:
            print("not valid key was sent motor will stop")
            self.motor_vel.data=0
        print(self.motor_vel)



    def cleanup(self):
        #This function is called just before finishing the node
        # You can use it to clean things up before leaving
        # Example: stop the robot before finishing a node.
        vel=Int32()
        vel.data=0
        self.pub_motor_vel.publish(vel)


############################### MAIN PROGRAM ####################################

if __name__ == "__main__":
    rospy.init_node("motor_controller", anonymous=True)
    try:
        MotorController()
    except:
        rospy.logfatal("motor_controller died")
