#! /usr/bin/env python
import rospy, time, math
from geometry_msgs.msg import Twist

def move_line():
    rospy.init_node('twist_publisher')
    twist = Twist()
    twist.angular.z = 0
    twist.linear.x = 0.1
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
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(2)
    start = time.time()
    while not rospy.is_shutdown() and time.time() - start < 15:
        pub.publish(twist)
        r.sleep()
    twist.angular.z = 0.0
    twist.linear.x = 0.0
    pub.publish(twist)

    print('COMPLETE')

# Added funcs for rotating and moving in a line for a known distance
def rotate(twist, pub, r, angle):
    twist.angular.z = 0.0
    twist.linear.x = 0.0
    pub.publish(twist)

    start = rospy.get_time()
    angle_rotated = 0.0
    while not rospy.is_shutdown() and (angle_rotated <= 1):
        twist.angular.z = angle
        twist.linear.x = 0.0
        pub.publish(twist)
        r.sleep()
        angle_rotated = rospy.get_time() - start 

    twist.angular.z = 0.0
    twist.linear.x = 0.0
    pub.publish(twist)

def move_straight(twist, pub, r, distance):
    twist.angular.z = 0.0
    twist.linear.x = 0.0
    pub.publish(twist)

    start = rospy.get_time()
    distance_travelled = 0.0
    while not rospy.is_shutdown() and (distance_travelled <= 1.0):
        twist.angular.z = 0.0
        twist.linear.x = distance
        pub.publish(twist)
        r.sleep()
        distance_travelled = rospy.get_time() - start

    twist.angular.z = 0.0
    twist.linear.x = 0.0
    pub.publish(twist)

def move_square():
    rospy.init_node('twist_publisher')
    twist = Twist()
    twist.angular.z = 0.0
    twist.linear.x = 0.0
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(10)

    move_straight(twist, pub, r, 0.75)
    r.sleep()
    for _ in range(3):
        rotate(twist, pub, r, math.pi/2)
        r.sleep()
        move_straight(twist, pub, r, 0.75)
        r.sleep()
    
    twist.angular.z = 0.0
    twist.linear.x = 0.0
    pub.publish(twist)

    print('COMPLETE')

def move_MShape():
    rospy.init_node('twist_publisher')
    twist = Twist()
    twist.angular.z = 0.0
    twist.linear.x = 0.0
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(10)
    
    move_straight(twist, pub, r, 0.75)
    r.sleep()
    rotate(twist, pub, r, 4 * math.pi / 3)
    r.sleep()
    move_straight(twist, pub, r, 0.5)
    r.sleep()
    rotate(twist, pub, r, -math.pi / 2)
    r.sleep()
    move_straight(twist, pub, r, 0.5)
    r.sleep()
    rotate(twist, pub, r, 4 * math.pi / 3)
    r.sleep()
    move_straight(twist, pub, r, 0.75)

    print('COMPLETE')

if __name__ == "__main__":
    #move_line()
    #move_circle()
    #move_square()
    move_MShape()