#!/usr/bin/env python
""" This program subscribes to a topic called input and publishes to output
    output and input supports Int32 messages; output will be input+10
    published topic:
        /output
    subscribed topics:
        /input
"""

import rospy
from std_msgs.msg import Int32

##### Global Variables ######
number=Int32()

def input_callback(msg):
    global number
    number=msg

def publish_sub():
    rospy.init_node('publish_sub', anonymous=True)  
    print("publish_sub initialized")
    pub = rospy.Publisher('output', Int32, queue_size=10)
    rospy.Subscriber('input', Int32, input_callback)
    global number
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub.publish(number.data+10)
        rate.sleep()

################  MAIN PROGRAM ###################### 
if __name__ == "__main__":
    try: 
        publish_sub() 
    except: 
        rospy.logfatal("publish sub died") 
