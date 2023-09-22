import rospy
from mavros_msgs.msg import  WaypointReached, ParamValue
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from mavros_msgs.srv import ParamSet
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QVBoxLayout
import cv2
import datetime as d
from Database.telemetria import telemetria
from config_module import config_module
import os

from diagnostic_msgs.msg import DiagnosticArray
from sensor_msgs.msg import CameraInfo
from Database.foto.foto import foto
from sensores import CustomFrames

class communication_module():


    def __init__(self, parent,telemetria,dron,foto,ns,config, flag_insertTelemetria, frame):
            self.config= config
            self.main = parent
            self.telemetria = telemetria
            self.v_telemetria = []
            self.fotos=[]
            self.dron = dron
            self.foto = foto
            self.ns = ns
            self.Posicion = ["null","null","null"]
            self.flag_insertTelemetria_c = int(ns[4])
            self.flag_insertTelemetria = flag_insertTelemetria
            self.n_canales = 1
            self.frame = frame
            print("He ingresado!!")


            #rospy.init_node('srvComand_node', anonymous=True)
            rospy.Subscriber("diagnostics", DiagnosticArray,self.drone_data)
           
            rospy.Subscriber("/"+self.ns+"/mavros/camera/camera_info", CameraInfo, self.camera_callback)
            rospy.Subscriber("/"+self.ns+"/mavros/global_position/raw/fix", NavSatFix, self.globalPositionCallback)
            rospy.Subscriber("/"+self.ns+"/mavros/imu/data", Imu, self.imu_callback)
            rospy.Subscriber("/"+self.ns+"/mavros/mission/reached", WaypointReached, self.waypoint_reached_callback)
            rospy.Subscriber("/"+self.ns+"/mavros/camera/image_raw",  Image, self.image_callback)
            self.dron_info()
            self.main.drone_1.setIcon(QIcon('./icons/drone_ok.svg'))
            
    def create_folder(self, path):
        try:
            # If the folder does not exist, create it
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            print("An error occurred while creating folder: ", e)

    def waypoint_reached_callback(self, msg):
        Path = "Images/mission:"+str(self.dron.get_id_mision())
        self.create_folder(Path)
        timestamp=d.datetime.now()
        hora_captura = timestamp.strftime("%H:%M:%S")
        try:
            # Convert your ROS Image message to OpenCV2
            cv2_img = CvBridge().imgmsg_to_cv2(self.image, "bgr8")
        except CvBridgeError as e:
            print(e)
        else:
            # Save your OpenCV2 image as a jpeg 
            cv2.imwrite(Path+"/"+str(self.dron.get_id_dron())+"_"+str(hora_captura)+".jpg", cv2_img)

        # TO DO: Agregar cordenadas y hora de captura
        self.foto.set_id_dron(self.dron.get_id_dron())
        self.foto.set_hora_captura(hora_captura)
        self.foto.set_latitud_captura(self.telemetria.get_latitud())
        self.foto.set_longitud_captura(self.telemetria.get_latitud())
        self.foto.set_altitud_captura(self.telemetria.get_latitud())
        self.fotos.append(self.foto)

    def image_callback(self, image):
        self.image = image
        
        
    def imu_callback(self,data):
        roll = data.orientation.x
        pitch = data.orientation.y
        yaw = data.orientation.z
        self.telemetria.set_cabeceo(pitch)
        self.telemetria.set_guinada(yaw)
        self.telemetria.set_alabeo(roll)

    def globalPositionCallback(self,globalPositionCallback):
        latitude = globalPositionCallback.latitude
        longitude = globalPositionCallback.longitude
        altitude = globalPositionCallback.altitude
        timestamp=d.datetime.now()
        hora_actualizacion = timestamp.strftime("%H:%M:%S")
        

        self.Posicion[0] = latitude
        self.Posicion[1] = longitude
        self.Posicion[2] = altitude
        self.telemetria.set_latitud(latitude)
        self.telemetria.set_longitud(longitude)
        self.telemetria.set_altitud(altitude)
        self.telemetria.set_hora_actualizacion(hora_actualizacion)
        
        self.main.tableWidget.setItem(0, 0, QTableWidgetItem(str(self.dron.get_hardware_id())))
        for item in range(3):
            self.main.tableWidget.setItem(0, item+1, QTableWidgetItem(str(self.Posicion[item])))
        #self.main.tableWidget.repaint()


        if(self.main.flag_telemetria==1):
            self.v_telemetria.append(self.telemetria)
            if(len(self.v_telemetria)>=10 and self.flag_insertTelemetria['valor'] == self.flag_insertTelemetria_c):
                self.config.insertar_telemetria(self.v_telemetria)
                self.v_telemetria = []
                if(self.n_canales ==self.flag_insertTelemetria['valor']):
                    self.flag_insertTelemetria['valor'] = 1
                else:
                    self.flag_insertTelemetria['valor']= self.flag_insertTelemetria['valor']+1


    def setFlightParameters(self, parameters):
        params_to_set = {                  # Increment  Range    Units
            'WPNAV_ACCEL' : parameters[0], #   10       50-500   cm/s^2 
            'WPNAV_SPEED' : parameters[1], #   50       20-2000  cm/s
            'WPNAV_SPEED_DN': 300,          #   10       10-500  cm/s
            'RTL_ALT_FINAL': 0 # cm
        }
        for id, value in params_to_set.items():
            if not self.set_param(id, value):
                print("Falla al poner el parametro %s" %id)
        
    def set_param(self, id, value):
        rospy.wait_for_service("/"+self.ns+"/mavros/param/set")
        try:
            set_param_srv = rospy.ServiceProxy("/"+self.ns+"/mavros/param/set",ParamSet)
            param_value = ParamValue()
            param_value.integer = int(value)
            resp = set_param_srv(id, param_value)
            return resp.success
        except rospy.ServiceException as e:
            print("Fallo al llamar el servicio: %s" %e)

    def dron_info(self):
        dron=self.ns[-1]
        rospy.Subscriber("/"+self.ns+"/mavros/camera/camera_info", CameraInfo, self.camera_callback)
        
        #self.frame.button2.setText("Conectado")


    def camera_callback(self, data):
        height = data.height
        if height != "null":
            self.telemetria.set_salud_camara("Ok")
            self.frame.cameraBtn.setIcon(QIcon('./icons/cameraVerde.svg'))
        else:
            self.frame.cameraBtn.setIcon(QIcon('./icons/cameraRojo.svg'))
        
    def drone_data(self,data):
        salud_gyro = ""
        salud_acelerometro = ""
        salud_magnetometro = ""
        salud_presion = ""
        for item in data.status:

            if item.name == self.ns+'/mavros: Heartbeat':
                    id = item.hardware_id
                    self.dron.set_hardware_id(id)

                    for v in item.values:
                        if v.key == 'Vehicle type':
                            self.dron.set_tipo(v.value)
                            self.telemetria.set_salud_controladora("Ok")

                        if v.key == 'Autopilot type':
                            self.dron.set_controladora(v.value)


            if item.name == self.ns+"/mavros: Battery":
                for value in item.values:
                    if value.key == "Voltage":
                        self.dron.set_voltaje_inicial(str(value.value))
                    if value.key == "Remaining":
                        porcentaje = value.value
                        self.telemetria.set_porcentaje_bateria(porcentaje)


            if item.name == self.ns+"/mavros: System":
                for value in item.values:
                    if value.key == "Battery":
                        if value.value == "Ok":
                            self.telemetria.set_salud_bateria(value.value)
                            self.frame.batteryBtn.setIcon(QIcon('./icons/batteryVerde.svg'))
                        else:
                            self.frame.batteryBtn.setIcon(QIcon('./icons/batteryRojo.svg'))
                    if value.key == "GPS":
                        if value.value == "Ok":
                            self.telemetria.set_salud_gps(value.value)
                            self.frame.gpsBtn.setIcon(QIcon('./icons/gpsVerde.svg'))
                        else:
                            self.frame.gpsBtn.setIcon(QIcon('./icons/gpsRojo.svg'))           
                    if value.key == "motor outputs / control":
                        if value.value == "Ok":
                            self.telemetria.set_salud_motores(value.value)
                            self.frame.motorBtn.setIcon(QIcon('./icons/motorVerde.svg'))
                        else:
                            self.frame.motorBtn.setIcon(QIcon('./icons/motorRojo.svg'))
                    if value.key == "rc receiver":
                        if value.value == "Ok":
                            self.frame.autopilotBtn.setIcon(QIcon('./icons/cpuVerde.svg'))
                        else:
                            self.frame.autopilotBtn.setIcon(QIcon('./icons/cpuRojo.svg'))
                    if value.key == "3D gyro":
                        salud_gyro = value.value
                    if value.key == "3D magnetometer":
                        salud_magnetometro = value.value
                    if value.key == "3D accelerometer":
                        salud_acelerometro = value.value
                    if value.key == "absolute pressure":
                        salud_presion = value.value

                    if salud_gyro == "Ok" and salud_magnetometro == "Ok" and salud_acelerometro == "Ok" and salud_presion == "Ok":
                        self.telemetria.set_salud_imu("Ok")
                        self.frame.imuBtn.setIcon(QIcon('./icons/imuVerde.svg'))
                    else:
                        self.frame.imuBtn.setIcon(QIcon('./icons/imuRojo.svg'))
        rospy.sleep(1)