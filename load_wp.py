#!/usr/bin/env python
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
from mavros_msgs.msg import WaypointList, Waypoint, State
from geometry_msgs.msg import PoseStamped

desired_altitude = 1

# Inicializar el nodo de ROS
rospy.init_node('mission_node')

# Modo ESTABLE
print("Activando modo Estable")
rospy.wait_for_service('/mavros/set_mode')
try:
    flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
    #http://wiki.ros.org/mavros/CustomModes for custom modes
    isModeChanged = flightModeService(custom_mode='STABILIZE') #return true or false
except rospy.ServiceException as e:
    print("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)

# Armar el drone
rospy.wait_for_service('/mavros/cmd/arming')
arm_service = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
arm_response = arm_service(True)
print("armando dron")

# Esperar a que el drone este armado
rate = rospy.Rate(10) # 10 Hz
while not rospy.is_shutdown():
    state = rospy.wait_for_message('/mavros/state', State, timeout=5)
    if state.armed:
        rospy.loginfo('Drone ARMED')
        print("Dron armado")
        break
    rate.sleep()

# Modo automatico
print("Activando modo GUIADO")
rospy.wait_for_service('/mavros/set_mode')
try:
    flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
    #http://wiki.ros.org/mavros/CustomModes for custom modes
    isModeChanged = flightModeService(custom_mode='GUIDED') #return true or false
except rospy.ServiceException as e:
    print("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)

# Despegar
print("despegando dron")
rospy.wait_for_service('/mavros/cmd/takeoff')

try:
    takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL) 
    takeoff_response = takeoffService(altitude = desired_altitude, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
except rospy.ServiceException as e:
    print ("Service takeoff call failed: %s"%e)

# Esperar a que el drone alcance la altitud deseada

# Callback function for pose data
def pose_callback(data):
    global current_altitude
    current_altitude = data.pose.position.z
    
desired_altitude = 1.0
global current_altitude
current_altitude = None
rospy.Subscriber('/mavros/local_position/pose', PoseStamped, pose_callback)
while current_altitude is None or current_altitude < desired_altitude:
    print(current_altitude)
    rospy.sleep(0.1)


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
#rospy.init_node('waypoint_publisher')

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


# Modo automatico
print("Activando modo AUTO")
rospy.wait_for_service('/mavros/set_mode')
try:
    flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
    #http://wiki.ros.org/mavros/CustomModes for custom modes
    isModeChanged = flightModeService(custom_mode='AUTO') #return true or false
except rospy.ServiceException as e:
    print("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)