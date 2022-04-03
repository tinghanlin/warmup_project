#!/usr/bin/env python3

import rospy

# msgs needed for /cmd_vel
from geometry_msgs.msg import Twist, Vector3

class DriveSquare(object):
    """ This node drives the robot in a square, in a right direction"""

    def __init__(self):
        # initialize the ROS node
        rospy.init_node('drive_square')
        # setup publisher to the cmd_vel ROS topic
        self.robot_movement_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    def run(self):
        # setup the Twist message that moves the robot forward
        move_forward = Twist(
            linear=Vector3(0.5, 0, 0),
            angular=Vector3(0, 0, 0)
        )

        # allow the publisher enough time to set up before publishing the first msg
        rospy.sleep(1)

        # publish the message
        self.robot_movement_pub.publish(move_forward)


        turn_right = Twist(
            linear=Vector3(0, 0, 0),
            angular=Vector3(0, 0, -1.60)
        )

        rospy.sleep(1)

        self.robot_movement_pub.publish(turn_right)

        rospy.sleep(1)

        self.robot_movement_pub.publish(move_forward)

        rospy.sleep(1)
        
        stop = Twist(
            linear=Vector3(0, 0, 0),
            angular=Vector3(0, 0, 0)
        )

        self.robot_movement_pub.publish(stop)




        

        


if __name__ == '__main__':
    # instantiate the ROS node and run it
    node = DriveSquare()
    node.run()