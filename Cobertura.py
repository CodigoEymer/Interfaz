#!/usr/bin/env python
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
from mavros_msgs.msg import WaypointList, Waypoint, State, WaypointReached
from geometry_msgs.msg import PoseStamped

desired_altitude = 1


class StartMission():

    def __init__(self,lista_wp, progress_bar):
        
        self.progress_bar = progress_bar
        # Inicializar el nodo de ROS
        #rospy.init_node('mission_node_Start')

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
            
        global current_altitude
        current_altitude = None
        rospy.Subscriber('/mavros/local_position/pose', PoseStamped, pose_callback)
        while current_altitude is None or current_altitude < desired_altitude:
            print(current_altitude)
            rospy.sleep(0.1)


        # Define waypoints
        waypoints = []

        for wp in lista_wp:
            latitud = wp[0]
            longitud = wp[1]
            print({latitud}, {longitud})

            wp = Waypoint()
            wp.frame = 3 # MAV_FRAME_GLOBAL_RELATIVE_ALT
            wp.command = 16 # MAV_CMD_NAV_WAYPOINT
            wp.is_current = False
            wp.autocontinue = True
            wp.x_lat = latitud # Latitud en grados
            wp.y_long = longitud # Longitud en grados
            wp.z_alt = 10 # Altitud en metros
            waypoints.append(wp)

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

        self.progress_bar.setMaximum(len(lista_wp)-1)
        print("n_wp",len(lista_wp)-1)

        def callback(data):
            rospy.loginfo(rospy.get_caller_id() + " Waypoint reached: %d", data.wp_seq)
            
            self.progress_bar.setValue(data.wp_seq)


        rospy.Subscriber("mavros/mission/reached", WaypointReached, callback)