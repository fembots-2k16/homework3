#!/usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def processPose(pose_msg):
    pose = pose_msg.pose.pose.position
    print "odom: " + str(pose.x) + ", " + str(pose.y)

def processGps(gps_msg):
    linear = gps_msg.twist.linear
    print "gps: " + str(linear.x) + ", " + str(linear.y)

def main():
    ns = "r0"
    pose_sub = rospy.Subscriber('/odom', Odometry, processPose)
    gps_sub = rospy.Subscriber('/base_pose_ground_truth', Twist, processGps)

    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    time = 0

    rospy.init_node('navigator')
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        time += 1
        twist = Twist() #values default to 0 when new instance initiated
        twist.linear.x = 1.0

        #publish the message
        vel_pub.publish(twist)
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
