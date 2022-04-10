# warmup_project

## Robot Behavior

### Driving in a Square
* High-level Description

  The task is to drive the robot in a square, so I wrote my code to drive the robot in a square clockwise. The robot would first move forward, then turn right 90 degrees. These two actions would be completed by the robot for 4 times (see the following graph). By the time that the robot drives in a square, the robot will stop at its initial location. 
 
  <img src="drive_square_illustration.png" width="300" height="300" />



* Code explanation

  I created a node called DriveSquare(), which drives the robot in a square clockwise. In the node, I initialized the ROS node and set up a publisher for the cmd_vel ROS topic. Then, I defined the run function and set up three kinds of the Twist messages: move forward, turn right 90 degrees, and stop. To drive the robot in a square, I published the messages with one-second intervals and let the robot move forward and turn right (each for 4 times) and stop at the end.

* Gif 

  ![Alt Text](drive_square.gif)

### Person Follower
* High-level Description

  The task is to drive the robot and let it follow a person. To implement this task, I use the robot's laser scan sensors to find where the person is located relative to the robot. Then, I transform that angle to a turning angle (either clockwise or counterclockwise) so that the robot can turn it heads towards to the person. If the person is 3 meters directly behind the robot, the robot would turn 180 degree clockwise to face the person. While trying to face the person, the robot also maintains a constant linear force going forward.
 
* Code explanation

  I created a node called PersonFollower(), which drives the robot to follow a person. In the node, I initialized the ROS node and set up a publisher for the cmd_vel ROS topic and a subscriber for the scan ROS topic. Then, I defined a process_scan function where I examined the laser scanner data. I replaced 0.0 values in scanner data by another value and found the next smallest obstacle distance and its degree. With this information, I converted the LiDAR degrees from 0 - 359 to turning angles (see the following graph). For example, degrees from 0 - 90 is 0 to -90 (i.e. clockwise or turn right) and 360 - 270 is 0 to 90  (i.e. counterclockwise or turn left). Finally, I used this information to implement proportional control to publish messages to the robot and let the it follow the person.
  
  <img src="degree-to-angle.png" width="600" height="300" />
  

* Gif 

  ![Alt Text](person_follower.gif)

### Wall Follower
* High-level Description

  The task is to drive the robot to a wall and let it follow alongside the wall, which can have all kinds of corners. To solve this task, I first let the robot navigate to the closest wall (see left hand side of the following graph). Once the robot is 0.6 meters away from the wall, I let the robot turn counterclockwise and ensure its LiDAR 90 degree is the closest to the wall through proportional control (see right hand side of the following graph). With this implementation, the robot can follow the sides of the wall at a fixed distance indefinitely. 

 <img src="wall_follower_illustration.png"/>

* Code explanation

  I created a node called WallFollower(), which lets the robot to follow alongside the wall. In the node, I initialized the ROS node and set up a publisher for the cmd_vel ROS topic and a subscriber for the scan ROS topic. Similar to Person Follower, I defined a process_scan function where I examined the laser scanner data. When the robot is more than 0.6 meter away from a wall, the robot would use proportional control with desired set-point equal to 0 degree to travel to the nearest wall. Once the robot is 0.6 meters away from the wall, the robot would again use proportional control but with a desired set-point equal to 90 degrees. This means that robot's 90 degree will always be the closest to the wall while following the wall.
  
* Gif 

  ![Alt Text](wall_follower.gif)![Alt Text](wall_follower_2.gif)
## Challenges: 
* Computer Setup: I encountered many challenges using Virtual Box VM to control the robot. I would experience sudden extreme lags every hour and would be forced to send the shutdown signal to the VM. causing my temporary work not to be saved. Thanks to Colin, I am now able to use Virtual Box VM without experiencing extreme lags. Also thanks to David (TA), I am able to type even faster on the VM after adopting his tip in setting Virtual Box to low resolution mode.

* Person Follower: Originally, I had some difficulty understanding and interpreting the laser scan data. For example, I knew 0 degree is the front of the robot, but I didn't know what other degrees map to which directions. For another exmaple, I didn't understand why there were always 0.0 distance values in the scanner data. Luckily, I was able to resovle these challegnes from this Turtlebot3 website (https://emanual.robotis.com/docs/en/platform/turtlebot3/appendix_lds_01/) and understand 0.0 meaning in class and from the TA.

## Future work: 

### Driving in a Square
If I have more time, I will think about how to ensure the robot to stop at the exact same location where it starts to drive in the square. This would probably require putting marks on the ground and let the robot sense those location.

### Person Follower
I will think about how to change the robot's linear speed according to its distance to the person. For example, if the robot is far away from the person, I want the robot to "catch up" by moving faster towards the robot. If the robot is pretty close to the person, I want to the robot to move slower while following the person.

### Wall Follower
I will consider on how to improve the robot's behavior when it turns to follow a 90-degree angle of the wall. In the current implementation, the robot can turn and follow an inner 90-degree angle of the wall fairly decent (see the first turn in right hand side gif). However, the robot is not sharply following the outer 90-degree angle of the wall (see the right hand side gif). It looks the robot is traveling using a larger turning angle, which is something I wish to improve in the future. Also, I will think about to make the robot travel even closer (< 0.6 meters) to the wall to complete the same task. For example, I can stop the robot's linear speed when it is turning 90 degree instead of having a constant linear speed.

## Takeaways: 
* In order to control the robot, we need to setup a publisher and a subscriber. The publisher sends messages to the robot and tells the robot what to do next or where to move to. The subscriber receives the scans from the robot about its environment.
* It is important to give the robot some time in between two messages, so that the robot would have enough time to perform the task described in each message.
* The ranges field of the laser scan data is a list of 360 number where each number corresponds to the to the closest obstacle from the LiDAR at various angles. O degrees is head and it goes 360 degrees clockwise on the robot.
* When letting a robot follow a 90-degree wall at a constant speed, we need to ensure that it has enough space to make the turn, or else it is likely to hit the wall. 
