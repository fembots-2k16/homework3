#!/usr/bin/env python
import rospy
import math
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time

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
    hertz = 3 
    rate = rospy.Rate(hertz) # 5hz
    linear_amt_traveled = 0
    angular_amt_traveled = 0

    print "travel: " + str(linear_amt) + "m @ speed: " + str(linear_speed) + "m/s"

    twist = Twist() #values default to 0 when new instance initiated
    twist.linear.x = linear_speed
    twist.angular.z = angular_speed

    seconds = linear_amt / linear_speed #in seconds
    print "seconds to move: " + str(seconds)

    startTime = int(round(time.time() * 1000))
    print startTime
    maxi = int(round(seconds * hertz)) # max number of seconds
    maxTime = startTime + (maxi * 1000) # max number of milliseconds the robot should move for
    print "max seconds: " + str(maxi)
    print "max milliseconds: " + str(maxTime)
    curTime = int(round(time.time() * 1000)) # get current time
    while curTime < maxTime: # while current time is less than max time
        #print "i : " + str(i)
        #print "curTime " + str(curTime)
        #publish the message
        vel_pub.publish(twist)
        curTime = int(round(time.time() * 1000))
        rate.sleep() #

    millis = int(round(time.time() * 1000))
    print millis
    #rospy.sleep(3.0)
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
