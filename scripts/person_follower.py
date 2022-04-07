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

# How close we will get to wall.
distance = 0.4

class StopAtWall(object):
    """ This node walks the robot to follow a person """

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
        # Determine closeness to wall by looking at scan data from in front of
        #   the robot, set linear velocity based on that information, and
        #   publish to cmd_vel.


        # The ranges field is a list of 360 number where each number
        #   corresponds to the distance to the closest obstacle from the
        #   LiDAR at various angles. Each measurement is 1 degree apart.
        
        #need to count the second min value to 0.0

        print("print type",type(data.ranges))
        distance_ranges = list(data.ranges)

        for i in range(len(distance_ranges)):
            if distance_ranges[i] == 0.0:
                distance_ranges[i] = 10000000
        
        print(distance_ranges)
        min_value = min(distance_ranges)
        min_index = distance_ranges.index(min_value)

        print("min_index: ", min_index)
        #e(t) = (desired set-point) - (process variable)
        if 0 < min_index and min_index < 180:
            min_index= -min_index
        elif 180 < min_index and min_index <= 359:
            min_index= -(min_index -360)
        else: 
            min_index = min_index

        error = (0 - min_index)
        print("error: ", error)
        kp = 1.5*error
        print("kp: ", kp)
        
        print("radian: ", kp*(math.pi/180))
        self.twist.angular.z = kp*(math.pi/180)

        self.twist.linear.x = 0.5


        # The first entry in the ranges list corresponds with what's directly
        #   in front of the robot.
        # degree = 0
        # count = 0
        # degree_sum = 0
        # for degree_distance in data.ranges:
        #     print("degree_distance:",degree_distance)
        #     print("degree:",degree)
        #     if degree_distance > 0 and degree_distance < 0.5: 
        #         count+=1
        #         if 0 < degree and degree < 180:
        #             degree_sum+= -degree
        #         elif 180 < degree and degree <= 359:
        #             degree_sum+= -(degree -360)
        #         else: 
        #             degree_sum+= degree
        #     degree += 1
        # if count == 0:
        #     average_degree = 0
        # else:
        #     average_degree = degree_sum/count
        
        # print("average_degree:",average_degree)
        # print("angular:",(average_degree)*(math.pi/180))
        # self.twist.angular.z = (average_degree)*(math.pi/180)
        # self.twist.linear.x = 0.1
        # if (data.ranges[0] == 0.0 or data.ranges[0] >= distance):
        #     # Go forward if not close enough to wall.
        #     self.twist.linear.x = 0.1
            
            
        # else:
        #     # Close enough to wall, stop.
        #     self.twist.linear.x = 0

        # Publish msg to cmd_vel.
        self.twist_pub.publish(self.twist)


    def run(self):
        # Keep the program alive.
        rospy.spin()

if __name__ == '__main__':
    # Declare a node and run it.
    node = StopAtWall()
    node.run()