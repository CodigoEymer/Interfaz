#!/usr/bin/env python

import rospy
from mavros_msgs.msg import State, WaypointReached
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2

class DroneController:
    def __init__(self, waypoints):
        self.waypoints = waypoints
        rospy.init_node('drone_controller', anonymous=True)
        rate = rospy.Rate(20)

        self.current_state = State()
        self.current_location = NavSatFix()

        rospy.Subscriber("mavros/global_position/global", NavSatFix, self.location_cb)
        rospy.Subscriber("/mavros/mission/reached", WaypointReached, self.waypoint_reached_callback)
        
        self.current_waypoint_index = 0
        
        self.camera_pub = rospy.Publisher('camera/trigger', String, queue_size=10)  # topic to trigger camera


    def location_cb(self, msg):
        self.current_location = msg

    def waypoint_reached_callback(self, msg):
        print("Waypoint reached: %s" % msg.wp_seq)
        try:
            # Convert your ROS Image message to OpenCV2
            cv2_img = CvBridge().imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError, e:
            print(e)
        else:
            # Save your OpenCV2 image as a jpeg 
            cv2.imwrite('/home/pi/images/camera_image.jpeg', cv2_img)
