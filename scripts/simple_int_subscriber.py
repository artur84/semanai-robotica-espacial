#!/usr/bin/env python
""" This program subscribes to a given ROS topic
    Published topic:
        /number_topic
"""
import rospy
from std_msgs.msg import Int32

def my_callback(my_message):
    print("I received the following message", my_message.data)

def simple_subscriber():
    #### Init the Node        #####
    rospy.init_node('simple_int_subscriber', anonymous=True)  
    print("SimpleSubscriber initialized")
    #### Init the subscriber  #####
    rospy.Subscriber('number_topic', Int32, my_callback)
    rate = rospy.Rate(10) # 10hz
    rospy.spin()

################  MAIN PROGRAM ###################### 
if __name__ == "__main__":
    try: 
        simple_subscriber() 
    except: 
        rospy.logfatal("simple_int_subscriber died") 
