#!/usr/bin/env python
""" This node will send a combination of values between -255 to 255 to both rover wheels, 
        depending on the pressed key
        Author: Jesus Arturo Escobedo Cabello
    Published topics:
    - right_wheel_speed [Int32]
    - left_wheel_speed [Int32]
"""



import rospy
from std_msgs.msg import Int32
from copy import deepcopy
import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

+/- : increase/decrease max speeds


CTRL-C to quit
"""
#(left_speed right_speed)
moveBindings = {
    'i':( 1,     1),
    'o':( 1,   0.3),
    'l':( 1,    -1),
    '.':(-1,  -0.3),
    ',':(-1,    -1),
    'm':(-0.3,  -1),
    'j':( -1,    1),
    'u':( 0.3,   1),
    'k':( 0,     0),
       }

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

left_speed = 100 #left wheel speed multiplier
right_speed = 100 #right wheel speed multiplier
left_inc = 5 #increment for the angular vel when the +/- keys are pressed.
right_inc = 5 #increment for the linear vel when the +/- keys are pressed.

def vels(left, right):
    return "currently:\t left_wheel_speed: %s\t right_wheel_speed: %s" % (left, right)

if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('rover_teleop_key')
    """ ROS Parameters
    """
    right_wheel_speed_pub = rospy.Publisher('right_wheel_speed', Int32, queue_size=10)
    left_wheel_speed_pub = rospy.Publisher('left_wheel_speed', Int32, queue_size=10)

    left = 0
    right = 0
    status =0
    try:
        print msg
        print vels(left, right)
        left_msg = Int32()
        right_msg = Int32()
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                left = moveBindings[key][0]
                right = moveBindings[key][1]
                left_msg.data = int(left * left_speed)
                right_msg.data = int(right * right_speed)
                right_wheel_speed_pub.publish(right_msg)
                left_wheel_speed_pub.publish(left_msg)


            elif key == '+':
                if left_speed <=(255 - left_inc):
                    left_speed = left_speed + left_inc
                else:
                    left_speed=255
                    
                if right_speed <=(255 - right_inc):
                    right_speed = right_speed + left_inc
                else:
                    right_speed=255
                print vels(left_speed, right_speed)
                if (status == 14):
                    print msg
                status = (status + 1) % 15


            elif key == '-':
                if left_speed >=(-255 + left_inc):
                    left_speed = left_speed - left_inc
                else:
                    left_speed=-255
                    
                if right_speed >=(-255 + left_inc):
                    right_speed = right_speed - left_inc
                else:
                    right_speed=-255
                print vels(left_speed, right_speed)
                if (status == 14):
                    print msg
                status = (status + 1) % 15


            else:
                left = 0; right = 0
                if (key == '\x03'):
                    break



    except:
        rospy.loginfo("rover_control.py: exception")

    finally:
        left_msg = Int32()
        right_msg = Int32()

        left_msg.data = 0; right_msg.data= 0

        right_wheel_speed_pub.publish(right_msg)
        left_wheel_speed_pub.publish(left_msg)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
