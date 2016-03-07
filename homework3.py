#!/usr/bin/env python
import rospy
import math
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

odom = None
gps = None
def processPose(pose_msg):
    global odom
    odom = pose_msg.pose.pose
    #print "odom: " + str(pose.x) + ", " + str(pose.y)

def processGps(gps_msg):
    global gps
    gps = gps_msg.pose.pose
    #print "gps: " + str(gps.x) + ", " + str(gps.y)

def main():
    if len(sys.argv) != 5:
        print "please run with four command line arguments:"
        print "\t1. number of meters to travel"
        print "\t2. number of degrees to rotate"
        print "\t3. linear speed (meters/second)"
        print "\t4. angular speed (degrees/second)"
        sys.exit()
    linear_amt = float(sys.argv[1])
    angular_amt = float(sys.argv[2])
    linear_speed = float(sys.argv[3])
    angular_speed = float(sys.argv[4])

    ns = "r0"
    pose_sub = rospy.Subscriber('/odom', Odometry, processPose)
    gps_sub = rospy.Subscriber('/base_pose_ground_truth', Odometry, processGps)

    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.init_node('navigator')
    rate = rospy.Rate(10) # 10hz
    linear_amt_traveled = 0
    angular_amt_traveled = 0

    twist = Twist() #values default to 0 when new instance initiated
    twist.linear.x = linear_speed
    twist.angular.z = angular_speed

    for i in range(90):
        #publish the message
        if angular_amt_traveled >= angular_amt and linear_amt_traveled >= linear_amt:
            break
        else:
            vel_pub.publish(twist)

        rospy.sleep(0.1) #0.1 seconds?

        linear_amt_traveled += linear_speed*0.1
        angular_amt_traveled += angular_speed*0.1

    rospy.sleep(3.0)
    global gps
    global odom
    print "finished"
    print "--------------------------------------"
    print "gps: x: " + str(gps.position.x) + ", y: " + str(gps.position.y) + \
          ", theta: " + str(gps.orientation.z)
    print "odom: " + str(odom.position.x) + ", " + str(odom.position.y) + \
          ", theta: " + str(odom.orientation.z)

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
