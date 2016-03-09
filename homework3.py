#!/usr/bin/env python
import rospy
import math
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from gazebo_msgs.msg import ModelStates, ModelState

odom = None
gps = None
modelStates = None
foundPioneer = False 
pioneerIndex = -1 #index of the pioneer in the Model States data

def processPose(pose_msg):
    global odom
    odom = pose_msg.pose.pose
    #print "odom: " + str(pose.x) + ", " + str(pose.y)

def processGps(gps_msg):
    global gps
    gps = gps_msg.pose.pose

def findPioneer(state_msg):
    # loop through length of the model names and find the pioneer's index
    global pioneerIndex
    global foundPioneer
    names = state_msg.name
    for i in range(0, len(state_msg.name)):
        if (names[i] == 'pioneer'):
            pioneerIndex = i # set the pioneer's index in the data values
            foundPioneer = True
            print "found pioneer"

def processStates(state_msg):
    global i
    global modelStates
    global foundPioneer
    global pioneerIndex
    if (foundPioneer):
        modelStates = state_msg.pose[pioneerIndex]
    else:
        findPioneer(state_msg)
        modelStates = state_msg.pose[pioneerIndex]
        print "x: " + str(modelStates.position.x) + " y: " + str(modelStates.position.y) + " z: " + str(modelStates.orientation.z)
    
    
def main():
    if len(sys.argv) != 6:
        print "please run with five command line arguments:"
        print "\t1. number of meters to travel"
        print "\t2. number of degrees to rotate"
        print "\t3. linear speed (meters/second)"
        print "\t4. angular speed (degrees/second)"
        print "\t5. simulation environment (stage or gazebo)"
        sys.exit()
    linear_amt = float(sys.argv[1])
    angular_amt = (math.pi*float(sys.argv[2]))/180
    linear_speed = float(sys.argv[3])
    angular_speed = (math.pi*float(sys.argv[4]))/180
    fast_angle = (float(sys.argv[4]) > 100)
    simEnvironment = sys.argv[5]    

    ns = "r0"
    pose_sub = rospy.Subscriber('/odom', Odometry, processPose)
    if (simEnvironment == "stage"):
        gps_sub = rospy.Subscriber('/base_pose_ground_truth', Odometry, processGps)
    elif (simEnvironment == "gazebo"):
        state_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, processStates)

    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.init_node('navigator')

    rospy.sleep(1.0) #wait for our publishers/subscribers to connect
    hertz = 10
    rate = rospy.Rate(hertz) # 5hz

    print "travel: " + str(linear_amt) + "m @ speed: " + str(linear_speed) + "m/s"
    print "rotate: " + str(angular_amt) + "rad @ speed: " + str(angular_speed) + "rad/s"

    twist = Twist() #values default to 0 when new instance initiated
    twist.linear.x = linear_speed
    twist.angular.z = angular_speed*2

    seconds = 0
    dbl = 1
    if linear_speed != 0:
        seconds = linear_amt / linear_speed #in seconds
    else:
        seconds = angular_amt / (angular_speed)
        hertz = 5
        if fast_angle:
            hertz = 5
            dbl = 1.17

    maxi = int(round(seconds * hertz * dbl))
    for i in range(maxi):
        #publish the message
        vel_pub.publish(twist)
        rate.sleep() #
    vel_pub.publish(Twist())

    rospy.sleep(3.0)
    global modelStates
    global odom
    print "--------------end-results-----------------"
    print "odom: x: " + str(odom.position.x) + ", " + str(odom.position.y) + ", theta: " + str(odom.orientation.z)
    if (simEnvironment == "stage"):
        print "gps: x: " + str(gps.position.x) + ", y: " + str(gps.position.y) + \
          ", theta: " + str(gps.orientation.z)
    elif (simEnvironment == "gazebo"):
        print "model state: x: " + str(modelStates.position.x) + " y: " + str(modelStates.position.y) + \
            " z: " + str(modelStates.orientation.z)
    
if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
