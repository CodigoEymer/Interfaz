#!/usr/bin/env python
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
from mavros_msgs.msg import WaypointList, Waypoint, State, WaypointReached
from geometry_msgs.msg import PoseStamped


class Cobertura():

    def __init__(self,lista_wp, progress_bar,altura,wp_retorno_aut,wp_tramos):
        rospy.Subscriber('/mavros/local_position/pose', PoseStamped, self.pose_callback)
        rospy.Subscriber("mavros/mission/reached", WaypointReached, self.retorno)
        self.progress_bar = progress_bar
        self.lista_wp = lista_wp
        self.wp_tramos = wp_tramos
        self.n_tramos = len(self.wp_tramos)       
        self.altura = float(altura)
        self.current_altitude = None
        self.wp_retorno_aut = wp_retorno_aut
        self.tramo_actual = 0
        self.long_tramo = len(self.lista_wp)-1

    def StartMision(self):

        self.modo_estable()
        self.armar_dron()
        self.modo_guiado()
        self.despegar()
        if len(self.wp_retorno_aut)==0:
            self.set_wp(self.lista_wp)
            self.modo_automatico()
        else:
            self.set_wp(self.wp_tramos[self.tramo_actual])
            self.long_tramo = len(self.wp_tramos[self.tramo_actual])-1
            self.modo_automatico()

    def reanudar_mision(self):
        respuesta = ""
        self.tramo_actual=self.tramo_actual+1 
        if self.tramo_actual < self.n_tramos:               
            self.StartMision()
            respuesta = "Mision reanudada" 
            print(respuesta)       
            return respuesta
        else:
            respuesta = "No hay mas tramos"
            print(respuesta)
            return respuesta

    def retorno(self,data):
        self.progress_bar.setValue(data.wp_seq)
        print
        if data.wp_seq==self.long_tramo:
            self.modo_rtl()

    def pose_callback(self,data):
        self.current_altitude = data.pose.position.z  

    def modo_estable(self):
        print("Activando modo Estable")
        rospy.wait_for_service('/mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
            #http://wiki.ros.org/mavros/CustomModes for custom modes
            flightModeService(custom_mode='STABILIZE') #return true or false
        except rospy.ServiceException as e:
            print("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)

    def armar_dron(self):
        rospy.wait_for_service('/mavros/cmd/arming')
        arm_service = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        arm_service(True)
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

    def modo_guiado(self):

        print("Activando modo GUIADO")
        rospy.wait_for_service('/mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
            #http://wiki.ros.org/mavros/CustomModes for custom modes
            isModeChanged = flightModeService(custom_mode='GUIDED') #return true or false
        except rospy.ServiceException as e:
            print("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)

    def despegar(self):
        print("despegando dron")
        rospy.wait_for_service('/mavros/cmd/takeoff')

        try:
            takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL) 
            takeoff_response = takeoffService(altitude = self.altura, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
        except rospy.ServiceException as e:
            print ("Service takeoff call failed: %s"%e)

        # Esperar a que el drone alcance la altitud deseada

        while self.current_altitude is None or self.current_altitude < self.altura:
            rospy.sleep(0.1)

    def set_wp(self,lista_wp):
        waypoints = []

        for wp in lista_wp:
            latitud = wp[0]
            longitud = wp[1]

            wp = Waypoint()
            wp.frame = 3 # MAV_FRAME_GLOBAL_RELATIVE_ALT
            wp.command = 16 # MAV_CMD_NAV_WAYPOINT
            wp.is_current = False
            wp.autocontinue = True
            wp.x_lat = latitud # Latitud en grados
            wp.y_long = longitud # Longitud en grados
            wp.z_alt = self.altura # Altitud en metros
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

    def modo_automatico(self):
        print("Activando modo AUTO")
        rospy.wait_for_service('/mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
            #http://wiki.ros.org/mavros/CustomModes for custom modes
            flightModeService(custom_mode='AUTO') #return true or false
        except rospy.ServiceException as e:
            print("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)

        self.progress_bar.setMaximum(len(self.lista_wp)) 

    def modo_rtl(self):
        try:
            flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
            #http://wiki.ros.org/mavros/CustomModes for custom modes
            isModeChanged = flightModeService(custom_mode='RTL') #return true or false
        except rospy.ServiceException as e:
            print("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)
        