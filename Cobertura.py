#!/usr/bin/env python
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
from mavros_msgs.msg import WaypointList, Waypoint, State, WaypointReached
from geometry_msgs.msg import PoseStamped


class Cobertura():

    def __init__(self,lista_wp, progress_bar,altura,wp_retorno_aut,wp_tramos):
        rospy.Subscriber('/dron1/mavros/local_position/pose', PoseStamped, self.pose_callback)
        rospy.Subscriber("dron1/mavros/mission/reached", WaypointReached, self.retorno)
        self.progress_bar = progress_bar
        self.lista_wp = lista_wp
        self.wp_tramos = wp_tramos
        self.n_tramos = len(self.wp_tramos)       
        self.altura = float(altura)
        self.current_altitude = None
        self.wp_retorno_aut = wp_retorno_aut
        self.tramo_actual = 0
        self.long_tramo = len(self.lista_wp)-1
        self.respuesta = 0
        self.end=0
        self.msn_end_w = msn_end_w

    def estado_vuelo(self, state):
        if not state.armed and self.respuesta==1:
            self.msn_end_w.exec_()
            self.respuesta=0

    def StartMision(self):

        self.modo_estable()
        self.armar_dron()
        self.modo_guiado()
        self.despegar()
        if len(self.wp_retorno_aut)==0:
            self.set_wp(self.lista_wp)
            self.modo_automatico()
            self.respuesta = 1
        else:
            self.set_wp(self.wp_tramos[self.tramo_actual])
            self.long_tramo = len(self.wp_tramos[self.tramo_actual])-1
            self.modo_automatico()

    def reanudar_mision(self):
        self.tramo_actual=self.tramo_actual+1 
        if self.tramo_actual < self.n_tramos:               
            self.StartMision()
            if self.tramo_actual==self.n_tramos-1:
                self.respuesta = 1

    def retorno(self,data):
        text = "Waypoint alcanzado #"+ str(data.wp_seq)
        self.main.print_console(text)
        self.progress_bar.setValue(data.wp_seq)
        if data.wp_seq==self.long_tramo:
            self.main.print_console("Aterrizando")
            self.modo_land()
            

    def pose_callback(self,data):
        self.current_altitude = data.pose.position.z  

    def modo_estable(self):
        print("Activando modo Estable")
        rospy.wait_for_service('/dron1/mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('/dron1/mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='STABILIZE')
        except rospy.ServiceException as e:
            self.main.print_console("service set_mode call failed: %s. STABLE Mode could not be set. Check that GPS is enabled"%e)

    def armar_dron(self):
        rospy.wait_for_service('/dron1/mavros/cmd/arming')
        arm_service = rospy.ServiceProxy('/dron1/mavros/cmd/arming', CommandBool)
        arm_service(True)
        self.main.print_console("Armando motores")

        # Esperar a que el drone este armado
        rate = rospy.Rate(10) # 10 Hz
        while not rospy.is_shutdown():
            state = rospy.wait_for_message('/dron1/mavros/state', State, timeout=5)
            if state.armed:
                break
            rate.sleep()

    def modo_guiado(self):

        print("Activando modo GUIADO")
        rospy.wait_for_service('/dron1/mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('/dron1/mavros/set_mode', mavros_msgs.srv.SetMode)
            isModeChanged = flightModeService(custom_mode='GUIDED') 
        except rospy.ServiceException as e:
            self.main.print_console("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)

    def despegar(self):
        print("despegando dron")
        rospy.wait_for_service('/dron1/mavros/cmd/takeoff')

        try:
            takeoffService = rospy.ServiceProxy('/dron1/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL) 
            takeoff_response = takeoffService(altitude = self.altura, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
        except rospy.ServiceException as e:
            self.main.print_console ("Service takeoff call failed: %s"%e)

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

        # Publish waypoints to /dron1/mavros/mission/push
        wp_pub = rospy.Publisher('/dron1/mavros/mission/push', WaypointList, queue_size=10)

        # Wait for the service to become available
        rospy.wait_for_service('/dron1/mavros/mission/push')

        try:
            push_wp = rospy.ServiceProxy('/dron1/mavros/mission/push', WaypointPush)

            # Push the waypoints to Ardupilot
            push_wp(start_index=0, waypoints=waypoints)
            # Publish the waypoints to the topic
            wp_list = WaypointList()
            wp_list.waypoints = waypoints
            wp_pub.publish(wp_list)
            self.main.print_console("Waypoints cargados exitosamente")
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s"%e)

    def modo_automatico(self):
        print("Activando modo AUTO")
        rospy.wait_for_service('/dron1/mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('/dron1/mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='AUTO') 
        except rospy.ServiceException as e:
            self.main.print_console("service set_mode call failed: %s. AUTO Mode could not be set. Check that GPS is enabled"%e)

        self.progress_bar.setMaximum(len(self.lista_wp)) 

    def modo_rtl(self):
        try:
            flightModeService = rospy.ServiceProxy('/dron1/mavros/set_mode', mavros_msgs.srv.SetMode)
            isModeChanged = flightModeService(custom_mode='RTL') 
        except rospy.ServiceException as e:

            self.main.print_console("service set_mode call failed: %s. RTL Mode could not be set. Check that GPS is enabled"%e)

    def modo_land(self):

        print("Activando modo LAND")
        rospy.wait_for_service('/dron1/mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('/dron1/mavros/set_mode', mavros_msgs.srv.SetMode)
            isModeChanged = flightModeService(custom_mode='LAND') 
        except rospy.ServiceException as e:

            self.main.print_console("service set_mode call failed: %s. LAND Mode could not be set. Check that GPS is enabled"%e)