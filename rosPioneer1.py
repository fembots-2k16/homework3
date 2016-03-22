#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from p2os_msgs.msg import MotorState
from geometry_msgs.msg import Twist
from p2os_msgs.msg import SonarArray

def processOdometry(self, odoMsg):
    linear = odoMsg.pose.pose.position
    angular = odoMsg.pose.pose.orientation
    print "linear x=%0.2f, y=%0.2f, z=%0.2f" %(linear.x, linear.y, linear.z)
    print "angulr x=%0.2f, y=%0.2f, z=%0.2f, w=%0.2f" %(angular.x, angular.y, angular.z, angular.w)

def processSonar(self, sonMsg, sonLock):
    print sonMsg.ranges

if __name__ == "__main__":
    ns = "pioneer"
    sonSub = rospy.Subscriber("/sonar", SonarArray, processSonar)
    odoSub = rospy.Subscriber("/pose", Odometry, processOdometry)

    #publishers
    velPub = rospy.Publisher("/cmd_vel", Twist)
    motPub = rospy.Publisher("/cmd_motor_state", MotorState)

    rate = rospy.Rate(1)
    count = 0
    vel = Twist()
    vel.linear.x = 0.1

    motor = MotorState()
    motor.state = 1

    while not rospy.is_shutdown():
        motPub.publish(motor)
        velPub.publish(vel)
        rate.sleep()
        if count > 15:
            vel.linear.x = 0.0
            velPub.publish(vel)
            motor.state = 0
            motPub.publish(motor)
            break
        count += 1
