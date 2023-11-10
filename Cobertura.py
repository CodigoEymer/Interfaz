#!/usr/bin/env python
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
from mavros_msgs.msg import WaypointList, Waypoint, State, WaypointReached, StatusText, ParamValue
from geometry_msgs.msg import PoseStamped
class Cobertura():

    def __init__(self, parent, progress_bar,altura_segura,altura_wp,wp_retorno_aut,wp_tramos, ns):
        self.main = parent
        self.progress_bar = progress_bar
        self.wp_tramos = wp_tramos
        self.n_tramos = len(self.wp_tramos)       
        self.altura_wp = altura_wp
        self.altura_segura = altura_segura
        self.current_altitude = None
        self.wp_retorno_aut = wp_retorno_aut
        self.tramo_actual = 0
        self.respuesta = 0
        self.long_tramo = 0
        self.end=0
        self.ns = ns
        self.start_mision = 0
        self.fcolorposse = "/"
        self.nWpActual = 0
        self.frameEstados = None
        
        
    def status_callback(self, status):
        self.status = status
        

    def StartMision(self):
        self.nWpActual = 0
        self.start_mision = 1
        self.f_estable =1
        self.f_armar = 0
        self.f_guided =0
        self.f_despegar = 0
        self.f_land = 0
        rospy.Subscriber("/"+self.ns+"/mavros/local_position/pose", PoseStamped, self.pose_callback)
        rospy.Subscriber("/"+self.ns+"/mavros/mission/reached", WaypointReached, self.retorno)
        rospy.Subscriber("/"+self.ns+"/mavros/state", State,self.estado_vuelo)
        rospy.Subscriber("/"+self.ns+"/mavros/statustext/recv", StatusText,self.status_callback)
        


    def estado_vuelo(self,state):
        if self.frameEstados!=None:
            self.estado = state
            self.main.mode(self.frameEstados,self.estado.mode)
            if self.estado.armed==False and self.f_land==1:
                self.main.console(self.ns+": Desarmado")
                self.f_land = 0
            if self.estado.armed==False and self.respuesta==1:
                self.main.stop_all()
                self.respuesta=0
                
            if (self.start_mision == 1 ):
                if(self.f_estable ==1 and self.estado.armed==False):
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
                    self.formato_wp(self.wp_tramos[self.tramo_actual])
                    self.long_tramo = len(self.wp_tramos[self.tramo_actual])-1
                    self.modo_automatico()
                    if self.tramo_actual==self.n_tramos-1:
                        self.respuesta = 1
                    self.f_despegar = 0

    def reanudar_mision(self):
        self.tramo_actual=self.tramo_actual+1
        if self.tramo_actual < self.n_tramos:           
            self.start_mision = 1
            self.f_estable =1
            
    def retorno(self,data):
        text = self.ns+": Waypoint alcanzado #"+ str(data.wp_seq) 
        self.main.console(text)
        self.nWpActual = self.nWpActual+1
        self.frameEstados.progress_bar.setValue(self.nWpActual)
        self.main.update_progress_bar()
        if data.wp_seq==self.long_tramo+3:
            self.main.console(self.ns+": Aterrizando.")
            self.modo_land()
            self.start_mision = 0
            self.f_land = 1
            
        if data.wp_seq == 1:
            self.fcolorposse = "_"
        if data.wp_seq == self.long_tramo+2:
            self.fcolorposse = "/"
            

    def pose_callback(self,data):
        self.current_altitude = data.pose.position.z  

    def modo_estable(self):
        self.main.console(self.ns+": Activando modo ESTABLE")
        rospy.wait_for_service("/"+self.ns+"/mavros/set_mode")
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            flightModeService(custom_mode="STABILIZE")
        except rospy.ServiceException as e:
            self.main.console(self.ns+": Service set_mode call failed: %s. STABLE Mode could not be set. Check that GPS is enabled"%e)
        

    def armar_dron(self):
        rospy.wait_for_service("/"+self.ns+"/mavros/cmd/arming")
        arm_service = rospy.ServiceProxy("/"+self.ns+"/mavros/cmd/arming", CommandBool)
        arm_service(True)
        self.main.console(self.ns+": Armando motores.")

    def modo_guiado(self):

        self.main.console(self.ns+": Activando modo GUIADO.")
        rospy.wait_for_service("/"+self.ns+"/mavros/set_mode")
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            isModeChanged = flightModeService(custom_mode="GUIDED")
        except rospy.ServiceException as e:
            self.main.console(self.ns+": Service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)
        

    def despegar(self):
        self.main.console(self.ns+": Despegando.")
        rospy.wait_for_service("/"+self.ns+"/mavros/cmd/takeoff")

        try:
            takeoffService = rospy.ServiceProxy("/"+self.ns+"/mavros/cmd/takeoff", mavros_msgs.srv.CommandTOL) 
            takeoff_response = takeoffService(altitude = self.altura_segura, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
        except rospy.ServiceException as e:
            self.main.console (self.ns+": Service takeoff call failed: %s"%e)

        # Esperar a que el drone alcance la altitud deseada

        while self.current_altitude is None or self.current_altitude < self.altura_segura:
            rospy.sleep(0.1)

    def wp_a_waypoint(self, i, latitud, longitud,altitud):
        wp = Waypoint()
        wp.frame = 3 # MAV_FRAME_GLOBAL_RELATIVE_ALT
        wp.command = 16 # MAV_CMD_NAV_WAYPOINT
        if i == 0: wp.is_current = True
        else: wp.is_current = False
        wp.autocontinue = True
        #wp.param1 = 1 # Hover in sec
        wp.x_lat = latitud # Latitud en grados
        wp.y_long = longitud # Longitud en grados
        wp.z_alt = altitud # Altitud en metros
        
        return wp

    def formato_wp(self,lista_wp):
        waypoints = []
        wp = self.wp_a_waypoint(0,3.371387,-76.533004,0)
        waypoints.append(wp)     
        for i in range(len(lista_wp)): 
            latitud = lista_wp[i][0]
            longitud = lista_wp[i][1]
            if(i==len(lista_wp)-2 ):
                wp = self.wp_a_waypoint(i,latitud,longitud,self.altura_wp)
                waypoints.append(wp)
                wp = self.wp_a_waypoint(i,latitud,longitud,self.altura_segura)
            elif (i==len(lista_wp)-1):
                wp = self.wp_a_waypoint(i,latitud,longitud,self.altura_segura)
            elif i==0:
                wp = self.wp_a_waypoint(i,latitud,longitud,self.altura_segura)
                waypoints.append(wp)
                wp = self.wp_a_waypoint(i,latitud,longitud,self.altura_wp)
            else:
                wp = self.wp_a_waypoint(i,latitud,longitud,self.altura_wp)
            
            waypoints.append(wp)
        self.set_waypoint(waypoints)

    def set_waypoint(self, waypoints):

        # Wait for the service to become available
        rospy.wait_for_service("/"+self.ns+"/mavros/mission/push")
        try:
            push_wp = rospy.ServiceProxy("/"+self.ns+"/mavros/mission/push", WaypointPush)
            # Push the waypoints to Ardupilot
            respuesta=push_wp(start_index=0, waypoints=waypoints)
            flag=respuesta.success
            if flag:
                self.main.console(self.ns+": Waypoint cargado")
            else:
                self.main.console(self.ns+": Waypoint no cargados")
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s"%e)

    def modo_automatico(self):
        self.main.console(self.ns+": Activando modo AUTO")
        rospy.wait_for_service("/"+self.ns+"/mavros/set_mode")
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            flightModeService(custom_mode="AUTO")
        except rospy.ServiceException as e:
            self.main.console(self.ns+": Service set_mode call failed: %s. AUTO Mode could not be set. Check that GPS is enabled"%e)
        

        #self.progress_bar.setMaximum(len(self.lista_wp)) 

    def modo_rtl(self):
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            isModeChanged = flightModeService(custom_mode="RTL")
        except rospy.ServiceException as e:
            self.main.console(self.ns+": Service set_mode call failed: %s. RTL Mode could not be set. Check that GPS is enabled"%e)
         

    def modo_land(self):
        self.main.console(self.ns+": Activando modo LAND")
        rospy.wait_for_service("/"+self.ns+"/mavros/set_mode")
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            isModeChanged = flightModeService(custom_mode="LAND")
        except rospy.ServiceException as e:
            self.main.console(self.ns+": Service set_mode call failed: %s. LAND Mode could not be set. Check that GPS is enabled"%e)
        
            
    def frame_a_modificar(self, frame):
        self.frameEstados = frame


    def stop_mission(self):
        self.main.console(self.ns+": Configurando altura segura para RTL.")
        # Set the RTL altitude to the safe altitude
        #self.set_rtl_altitude(self.altura_segura)
        
        # Switch to RTL mode to return home
        self.activate_rtl_mode()
        
        # Reset mission parameters as needed
        self.cleanup_after_stop()

    # def set_rtl_altitude(self, alt):
    #     try:
    #         # Assuming there is a parameter set service to change the RTL altitude
    #         set_param_service = rospy.ServiceProxy("/"+self.ns+"/mavros/param/set", ParamSet)
    #         # The parameter name for RTL altitude may vary depending on the flight stack
    #         param_id = "RTL_ALTITUDE" # This is an example, the actual parameter ID may be different
    #         set_param_service(param_id=param_id, value=ParamValue(integer=0, real=alt))
    #     except rospy.ServiceException as e:
    #        self.main.console(self.ns+": Failed to set RTL altitude: %s"%e)

    def activate_rtl_mode(self):
        try:
            flightModeService = rospy.ServiceProxy("/"+self.ns+"/mavros/set_mode", mavros_msgs.srv.SetMode)
            flightModeService(custom_mode="RTL")
            self.main.console(self.ns+": Modo RTL activado.")
        except rospy.ServiceException as e:
            self.main.console(self.ns+": Service set_mode call failed: %s. RTL Mode could not be set. Check that GPS is enabled"%e)

    def cleanup_after_stop(self):
        self.start_mision = 0
        self.tramo_actual = 0
        self.nWpActual = 0
        # Update the progress bar or any GUI elements if necessary
        self.progress_bar.setValue(0)
        self.main.update_progress_bar()