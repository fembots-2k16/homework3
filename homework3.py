#!/usr/bin/env python
import rospy
import math
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def processPose(pose_msg):
    pose = pose_msg.pose.pose.position
    #print "odom: " + str(pose.x) + ", " + str(pose.y)

def processGps(gps_msg):
    gps = gps_msg.pose.pose.position
    #print "gps: " + str(gps.x) + ", " + str(gps.y)

def main():
    if len(sys.argv) != 3:
        print "please run with four command line arguments:"
        print "\t1. number of meters to travel"
        print "\t2. number of degrees to rotate"
        print "\t3. linear speed (meters/second)"
        print "\t4. angular speed (degrees/second)"
    linear_amt = float(sys.argv[1])
    angular_amt = float(sys.argv[2])
    linear_speed = float(sys.argv[3])
    angular_speed = float(sys.argv[4])

    ns = "r0"
    pose_sub = rospy.Subscriber('/odom', Odometry, processPose)
    gps_sub = rospy.Subscriber('/base_pose_ground_truth', Odometry, processGps)

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
