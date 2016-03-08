#!/usr/bin/env python
import rospy
import math
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from gazebo_msgs.msg import ModelStates

odom = None
model = None
def processPose(pose_msg):
    global odom
    odom = pose_msg.pose
    #print "odom: " + str(pose.x) + ", " + str(pose.y)

should_i_print = True
def processModelStates(mdl_msg):
    global model
    global should_i_print
    model = mdl_msg.pose
    if should_i_print:
        print model
        should_i_print = False

def main():
    if len(sys.argv) != 5:
        print "please run with four command line arguments:"
        print "\t1. number of meters to travel"
        print "\t2. number of degrees to rotate"
        print "\t3. linear speed (meters/second)"
        print "\t4. angular speed (degrees/second)"
        sys.exit()
    linear_amt = float(sys.argv[1])
    angular_amt = (math.pi*float(sys.argv[2]))/180
    linear_speed = float(sys.argv[3])
    angular_speed = (math.pi*float(sys.argv[4]))/180
    fast_angle = (float(sys.argv[4]) > 100)

    ns = "r0"
    pose_sub = rospy.Subscriber('/odom', Odometry, processPose)
    gps_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, processModelStates)


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
            hertz = 10
            dbl = 1.33

    maxi = int(round(seconds * hertz * dbl))
    for i in range(maxi):
        #publish the message
        vel_pub.publish(twist)
        rate.sleep() #
    vel_pub.publish(Twist())

    rospy.sleep(3.0)
    global odom
    global model
    print "--------------end-results-----------------"
    print "odom: " + str(model.position.x) + ", " + str(odom.position.y) + \
          ", theta: " + str(odom.orientation.z)
    print "gps: x: " + str(gps.position.x) + ", y: " + str(gps.position.y) + \
          ", theta: " + str(gps.orientation.z)

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
