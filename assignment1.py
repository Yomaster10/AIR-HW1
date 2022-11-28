#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time
import math
from tf.transformations import euler_from_quaternion


def l2_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


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
    # add a time stop to the circle run
    start = time.time()
    while not rospy.is_shutdown() and time.time() - start < 20:
        pub.publish(twist)
        r.sleep()
    # stop movement
    twist.angular.z = 0
    twist.linear.x = 0
    pub.publish(twist)
    print('COMPLETE')


# added funcs for turning and moving in a line for a known distance
def rotate(twist, pub, r, angle, counter=1, T_threshhold=0.005, k_turn=0.9):
    prev_error = 80
    while not rospy.is_shutdown() and (prev_error > T_threshhold or abs(angle - yaw) > T_threshhold):
        twist.angular.z = (angle - yaw) * k_turn if abs((angle - yaw) * k_turn) > 0.05 else 0.05 * counter
        twist.linear.x = 0
        pub.publish(twist)
        r.sleep()
        prev_error = abs(angle - yaw)
        twist.angular.z = 0
        twist.linear.x = 0
        pub.publish(twist)


def move_straight(twist, pub, r, distance=1, front=True, threshhold=0.05, kp_angle=0.9, kp=0.4):
    s_x, s_y = x, y
    s_yaw = yaw
    while not rospy.is_shutdown() and (l2_distance(s_x, s_y, x, y) < distance - threshhold):
        if front or abs((s_yaw - yaw)) < abs((s_yaw + yaw)):
            twist.angular.z = (s_yaw - yaw) * kp_angle
        else:
            twist.angular.z = - (s_yaw + yaw) * kp_angle
        twist.linear.x = (distance - l2_distance(s_x, s_y, x, y)) * kp  # 0.5
        pub.publish(twist)

        r.sleep()

    twist.angular.z = 0
    twist.linear.x = 0
    pub.publish(twist)


def move_square():
    def update(data):
        global x, y, yaw
        x, y = data.pose.pose.position.x, data.pose.pose.position.y
        (_, _, yaw) = euler_from_quaternion([data.pose.pose.orientation.x, data.pose.pose.orientation.z,
                                             data.pose.pose.orientation.z, data.pose.pose.orientation.w])
    rospy.init_node('twist_publisher')
    twist = Twist()
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    r = rospy.Rate(30)
    update()

    twist.angular.z = 0
    twist.linear.x = 0
    angles = [math.pi / 2, math.pi, -math.pi / 2, 0]
    pub.publish(twist)
    
    i = 0
    while i < 4:
        move_straight(twist, pub, r, yaw)
        rotate(twist, pub, r, angles[i])
        i += 1
    
    twist.angular.z = 0
    twist.linear.x = 0
    pub.publish(twist)

    print('COMPLETE')


def move_MShape():
    def update(data):
        global x, y, yaw
        x, y = data.pose.pose.position.x, data.pose.pose.position.y
        (_, _, yaw) = euler_from_quaternion([data.pose.pose.orientation.x, data.pose.pose.orientation.z,
                                             data.pose.pose.orientation.z, data.pose.pose.orientation.w])
    
    rospy.init_node('twist_publisher')
    twist = Twist()
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    r = rospy.Rate(30)
    update()
    
    move_straight(twist, pub, r, 0.7)
    rotate(twist, pub, r, 2 * math.pi / 3)
    move_straight(twist, pub, r, 0.7)
    rotate(twist, pub, r, math.pi / 3, -1)
    move_straight(twist, pub, r, 0.7)
    rotate(twist, pub, r, yaw, math.pi)
    move_straight(twist, pub, r, 0.7, False)

    print('COMPLETE')


if __name__ == "__main__":
    move_line()
    # move_circle()
    # move_square()
    # move_MShape()
