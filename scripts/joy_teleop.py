#!/usr/bin/env python
#include <sensor_msgs/Joy.h>
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
max_linear_velocity = 255
max_angular_velocity = 255

myTwist = Twist ()

def callback(data):
    myTwist.linear.x = max_linear_velocity * data.axes[1]
    myTwist.angular.z = max_angular_velocity * data.axes[0]





def joyListener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('joyTeleopNode', anonymous=True)

    rospy.Subscriber("joy", Joy, callback)
    pub = rospy.Publisher('joyTeleop', Twist, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub.publish(myTwist)
        rate.sleep()
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    joyListener()