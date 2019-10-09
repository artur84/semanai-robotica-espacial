#!/usr/bin/env python
""" This program publishes a given integer to a ROS topic
    The ROS topic is called number_topic
"""
import rospy
from std_msgs.msg import Int32

class SimplePublisher(): 
    def __init__(self): 
        print "SimplePublisher init"
        pub = rospy.Publisher('number_topic', Int32, queue_size=10)
        rate = rospy.Rate(10) # 10hz
        number = 0
        while not rospy.is_shutdown():
            pub.publish(number)
            number+=1
            if number >= 255:
                number=0
            rate.sleep()
    
    

################  MAIN PROGRAM ###################### 
if __name__ == "__main__":
    rospy.init_node('simple_int_publisher', anonymous=True) 
    try: 
        SimplePublisher() 
    except: 
        rospy.logfatal("simple_int_publisher died") 
