#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def move_line():
    rospy.init_node('twist_publisher')
    twist = Twist()
    twist.angular.z = 0 #0.5
    twist.linear.x = 0.5
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    r = rospy.Rate(2)
    while not rospy.is_shutdown(): 
        pub.publish(twist)
        r.sleep()

def move_circle():
    rospy.init_node('twist_publisher')
    twist = Twist()
    twist.angular.z = 0.5
    twist.linear.x = 0.5
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    r = rospy.Rate(2)
    while not rospy.is_shutdown(): 
        pub.publish(twist)
        r.sleep()

def move_square():
    print('COMPLETE')

if __name__ == "__main__":
    move_line()