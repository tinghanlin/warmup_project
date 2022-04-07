#!/usr/bin/env python3

# TOPICS:
#   cmd_vel: publish to, used for setting robot velocity
#   scan   : subscribing, where the person is

import rospy
import math

# msg needed for /scan.
from sensor_msgs.msg import LaserScan

# msgs needed for /cmd_vel.
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

class PersonFollower(object):
    """ This node controls the robot to follow a person """

    def __init__(self):
        # Start rospy node.
        rospy.init_node("person_follower")

        # Declare our node as a subscriber to the scan topic and
        #   set self.process_scan as the function to be used for callback.
        rospy.Subscriber("/scan", LaserScan, self.process_scan)

        # Get a publisher to the cmd_vel topic.
        self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

        # Create a default twist msg (all values 0).
        lin = Vector3()
        ang = Vector3()
        self.twist = Twist(linear=lin,angular=ang)

    def process_scan(self, data):
        # Determine where the person is using the 360 degree scan data and 
        # set the linear velocity and angular velocity.

        # The ranges field is a list of 360 number where each number
        # corresponds to the to the closest obstacle from the
        # LiDAR at various angles. Each measurement is 1 degree apart
        
        # data.ranges is a tuple object, so I convert it to a list
        # so that I can modify values in it.
        distance_ranges = list(data.ranges)

        # replace 0.0 by another value, I choose 10000000
        for i in range(len(distance_ranges)):
            if distance_ranges[i] == 0.0:
                distance_ranges[i] = 10000000
        
        # find the smallest obstacle distance and its degree
        # so I can later let the robot to follow this degree
        min_value = min(distance_ranges)
        min_index = distance_ranges.index(min_value)

        # convert the degrees from 0 - 359 to degrees for turning
        # for example, degrees from 0 - 180 is 0 to 90 and 359 - 180 is 0 to -90
        if 0 < min_index and min_index < 180:
            turning_degree= -min_index
        elif 180 < min_index and min_index < 360:
            turning_degree= -(min_index -360)
        else: 
            turning_degree = min_index
            
        # implement proportional control u(t) = Kp * e(t) to let the robot follow the person
        # e(t) = (desired set-point) - (process variable)
        # desired set-point is 0 because I want the head of the robot to follow the person
        # process variable is the turning degree
        error = (0 - turning_degree)
        
        # I choose a higher kp so that the robot can better adjust to the 
        # fact that the person movement is also dynamic
        kp = 1.5*error
        
        # convert turning degree to radian and set the twist message
        self.twist.angular.z = kp*(math.pi/180)
        self.twist.linear.x = 0.5
        self.twist_pub.publish(self.twist)


    def run(self):
        # Keep the program alive.
        rospy.spin()

if __name__ == '__main__':
    # Declare a node and run it.
    node = PersonFollower()
    node.run()
