#!/usr/bin/env python
import rospy
from mavros_msgs.msg import Waypoint, WaypointList
from mavros_msgs.srv import WaypointPush

# Define waypoints
waypoints = []
waypoints.append(Waypoint())
waypoints[0].frame = 3
waypoints[0].command = 16 # MAV_CMD_NAV_WAYPOINT
waypoints[0].is_current = False
waypoints[0].autocontinue = True
waypoints[0].x_lat = 37.7924881
waypoints[0].y_long = -122.3975057
waypoints[0].z_alt = 10

waypoints.append(Waypoint())
waypoints[1].frame = 3
waypoints[1].command = 16 # MAV_CMD_NAV_WAYPOINT
waypoints[1].is_current = False
waypoints[1].autocontinue = True
waypoints[1].x_lat = 37.7924981
waypoints[1].y_long = -122.3975157
waypoints[1].z_alt = 15

waypoints.append(Waypoint())
waypoints[2].frame = 3
waypoints[2].command = 16 # MAV_CMD_NAV_WAYPOINT
waypoints[2].is_current = False
waypoints[2].autocontinue = True
waypoints[2].x_lat = 37.7925081
waypoints[2].y_long = -122.3975257
waypoints[2].z_alt = 150
# Initialize node
rospy.init_node('waypoint_publisher')

# Publish waypoints to /mavros/mission/push
wp_pub = rospy.Publisher('/mavros/mission/push', WaypointList, queue_size=10)

# Wait for the service to become available
rospy.wait_for_service('/mavros/mission/push')

try:
    push_wp = rospy.ServiceProxy('/mavros/mission/push', WaypointPush)

    # Push the waypoints to Ardupilot
    push_wp(start_index=0, waypoints=waypoints)

    # Publish the waypoints to the topic
    wp_list = WaypointList()
    wp_list.waypoints = waypoints
    wp_pub.publish(wp_list)

    rospy.loginfo("Waypoints published successfully")

except rospy.ServiceException as e:
    rospy.logerr("Service call failed: %s"%e)
