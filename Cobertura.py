#!/usr/bin/env python
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
from mavros_msgs.msg import WaypointList, Waypoint, State, WaypointReached, StatusText
from geometry_msgs.msg import PoseStamped


class Cobertura():

    def __init__(self, parent, lista_wp, progress_bar,altura,wp_retorno_aut,wp_tramos, msn_end_w, ns):
        self.main = parent
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
        self.ns = ns
        self.start_mision = 0
        

    def status_callback(self, status):
        self.status = status
        # if not state.armed and self.respuesta==1:
        #     self.msn_end_w.exec_()
        #     self.respuesta=0

    def StartMision(self):
        self.start_mision = 1
        self.f_estable =1
        self.f_armar = 0
        self.f_guided =0
        self.f_despegar = 0
        rospy.Subscriber("/"+self.ns+"/mavros/local_position/pose", PoseStamped, self.pose_callback)
        rospy.Subscriber("/"+self.ns+"/mavros/mission/reached", WaypointReached, self.retorno)
        rospy.Subscriber("/"+self.ns+"/mavros/state", State,self.estado_vuelo)
        rospy.Subscriber("/"+self.ns+"/mavros/statustext/recv", StatusText,self.status_callback)
        


    def estado_vuelo(self,state):
        self.estado = state
        if self.start_mision == 1:

            if(self.f_estable ==1):
                self.modo_estable() 
                self.f_estable = 0
                self.armar_dron()
                self.f_armar = 1
            if(self.estado.armed and self.f_armar == 1):

                self.modo_guiado()
                self.f_armar = 0
                self.f_guided =1
            if(self.estado.guided and self.f_guided == 1):
                self.despegar()
                self.f_guided = 0
                self.f_despegar = 1
            if( self.f_despegar == 1 and "EKF3 IMU" in self.status.text and "yaw alignment complete" in self.status.text):
                if len(self.wp_retorno_aut)==0:
                    self.set_wp(self.lista_wp)
                    self.modo_automatico()
                    self.respuesta = 1
                else:
                    self.set_wp(self.wp_tramos[self.tramo_actual])
                    self.long_tramo = len(self.wp_tramos[self.tramo_actual])-1
                    self.modo_automatico()
                self.f_despegar = 0

    def reanudar_mision(self):
        self.tramo_actual=self.tramo_actual+1 
        if self.tramo_actual < self.n_tramos:               
            self.start_mision = 1
            self.f_estable =1
            if self.tramo_actual==self.n_tramos-1:
                self.respuesta = 1

    def retorno(self,data):
        text = self.ns+": Waypoint alcanzado #"+ str(data.wp_seq) 
        self.main.print_console(text)
        self.progress_bar.setValue(data.wp_seq)
        if data.wp_seq==self.long_tramo:
            self.main.print_console(self.ns+": Aterrizando.")
            self.modo_land()
            self.start_mision = 0
            

    def pose_callback(self,data):
        self.current_altitude = data.pose.position.z  

    def modo_estable(self):
        self.main.print_console(self.ns+": Activando modo ESTABLE")
        rospy.wait_for_service("/"+self.ns+"/mavros/set_mode")
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            flightModeService(custom_mode="STABILIZE")
        except rospy.ServiceException as e:
            self.main.print_console(self.ns+": Service set_mode call failed: %s. STABLE Mode could not be set. Check that GPS is enabled"%e)

    def armar_dron(self):
        rospy.wait_for_service("/"+self.ns+"/mavros/cmd/arming")
        arm_service = rospy.ServiceProxy("/"+self.ns+"/mavros/cmd/arming", CommandBool)
        arm_service(True)
        self.main.print_console(self.ns+": Armando motores.")

    def modo_guiado(self):

        self.main.print_console(self.ns+": Activando modo GUIADO.")
        rospy.wait_for_service("/"+self.ns+"/mavros/set_mode")
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            isModeChanged = flightModeService(custom_mode="GUIDED") 
        except rospy.ServiceException as e:
            self.main.print_console(self.ns+": Service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)

    def despegar(self):
        self.main.print_console(self.ns+": Despegando.")
        rospy.wait_for_service("/"+self.ns+"/mavros/cmd/takeoff")

        try:
            takeoffService = rospy.ServiceProxy("/"+self.ns+"/mavros/cmd/takeoff", mavros_msgs.srv.CommandTOL) 
            takeoff_response = takeoffService(altitude = self.altura, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
        except rospy.ServiceException as e:
            self.main.print_console (self.ns+": Service takeoff call failed: %s"%e)

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

        # Publish waypoints to /"+self.ns+"/mavros/mission/push
        wp_pub = rospy.Publisher("/"+self.ns+"/mavros/mission/push", WaypointList, queue_size=10)

        # Wait for the service to become available
        rospy.wait_for_service("/"+self.ns+"/mavros/mission/push")

        try:
            push_wp = rospy.ServiceProxy("/"+self.ns+"/mavros/mission/push", WaypointPush)

            # Push the waypoints to Ardupilot
            push_wp(start_index=0, waypoints=waypoints)
            # Publish the waypoints to the topic
            wp_list = WaypointList()
            wp_list.waypoints = waypoints
            wp_pub.publish(wp_list)
            self.main.print_console(self.ns+": Waypoints cargados exitosamente.")
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s"%e)

    def modo_automatico(self):
        self.main.print_console(self.ns+": Activando modo AUTO")
        rospy.wait_for_service("/"+self.ns+"/mavros/set_mode")
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            flightModeService(custom_mode="AUTO") 
        except rospy.ServiceException as e:
            self.main.print_console(self.ns+": Service set_mode call failed: %s. AUTO Mode could not be set. Check that GPS is enabled"%e)

        self.progress_bar.setMaximum(len(self.lista_wp)) 

    def modo_rtl(self):
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            isModeChanged = flightModeService(custom_mode="RTL") 
        except rospy.ServiceException as e:

            self.main.print_console(self.ns+": Service set_mode call failed: %s. RTL Mode could not be set. Check that GPS is enabled"%e)

    def modo_land(self):

        self.main.print_console(self.ns+": Activando modo LAND")
        rospy.wait_for_service("/"+self.ns+"/mavros/set_mode")
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            isModeChanged = flightModeService(custom_mode="LAND") 
        except rospy.ServiceException as e:

            self.main.print_console(self.ns+": Service set_mode call failed: %s. LAND Mode could not be set. Check that GPS is enabled"%e)