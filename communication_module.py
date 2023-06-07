import rospy
from mavros_msgs.msg import  WaypointReached, ParamValue
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from mavros_msgs.srv import ParamSet
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem
import cv2
import datetime as d
from Database.telemetria import telemetria
from config_module import config_module
import os

from diagnostic_msgs.msg import DiagnosticArray
from sensor_msgs.msg import CameraInfo
from Database.foto.foto import foto

class communication_module():

    Posicion = ["null","null","null"]

    def __init__(self, parent,telemetria,dron,fotos):
            self.main = parent
            self.telemetria = telemetria
            self.v_telemetria = []
            self.fotos=fotos
            self.dron = dron
            rospy.init_node('srvComand_node', anonymous=True)
            rospy.Subscriber("diagnostics", DiagnosticArray,self.drone_data)
            rospy.Subscriber("/mavros/camera/camera_info", CameraInfo, self.camera_callback)
            rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, self.globalPositionCallback)
            rospy.Subscriber("/mavros/imu/data", Imu, self.imu_callback)
            rospy.Subscriber("/mavros/mission/reached", WaypointReached, self.waypoint_reached_callback)
            rospy.Subscriber("/mavros/camera/image_raw",  Image, self.image_callback)
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
        foto_obj = foto()
        foto_obj.set_id_dron(self.dron.get_id_dron())
        foto_obj.set_hora_captura(hora_captura)
        foto_obj.set_latitud_captura(self.telemetria.get_latitud())
        foto_obj.set_longitud_captura(self.telemetria.get_longitud())
        foto_obj.set_altitud_captura(self.telemetria.get_altitud())
        self.fotos.append(foto_obj)
        print("fotos")
        print(len(self.fotos))

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

            if(len(self.v_telemetria)==10):
                self.main.config.insertar_telemetria(self.v_telemetria)
                self.v_telemetria = []

    def setFlightParameters(self, conf_module):
        parameters = conf_module.getParameters()
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
        rospy.wait_for_service('/mavros/param/set')
        try:
            set_param_srv = rospy.ServiceProxy('/mavros/param/set',ParamSet)
            param_value = ParamValue()
            param_value.integer = int(value)
            resp = set_param_srv(id, param_value)
            return resp.success
        except rospy.ServiceException as e:
            print("Fallo al llamar el servicio: %s" %e)

    def dron_info(self):
        dron=1
        rospy.Subscriber("diagnostics", DiagnosticArray,self.drone_data)
        rospy.Subscriber("/mavros/camera/camera_info", CameraInfo, self.camera_callback)
        
        conectado_status = "conectado_status" + str(dron)
        conectado = getattr(self.main,conectado_status)
        conectado.setText("Conectado")
		
        battery = "battery_good" + str(dron)
        self.batteryBtn = getattr(self.main, battery)
        self.battery_green = QIcon('./icons/batteryVerde.svg')
        self.battery_red = QIcon('./icons/batteryRojo.svg')
        self.batteryBtn.setIcon(self.battery_red)

        gps_good = "gps_good" + str(dron)
        self.gpsBtn = getattr(self.main, gps_good)
        self.gps_green = QIcon('./icons/gpsVerde.svg')
        self.gps_red = QIcon('./icons/gpsRojo.svg')
        self.gpsBtn.setIcon(self.gps_red) 
        
        motor_good = "motor_good" + str(dron)
        self.motorBtn = getattr(self.main, motor_good)
        self.motor_green = QIcon('./icons/motorVerde.svg')
        self.motor_red = QIcon('./icons/motorRojo.svg')
        self.motorBtn.setIcon(self.motor_red) 

        autopilot_good = "autopilot_good" + str(dron)
        self.autopilotBtn = getattr(self.main, autopilot_good)
        self.autopilot_green = QIcon('./icons/cpuVerde.svg')
        self.autopilot_red = QIcon('./icons/cpuRojo.svg')
        self.autopilotBtn.setIcon(self.autopilot_red) 


        imu_good = "imu_good" + str(dron)
        self.imuBtn = getattr(self.main, imu_good)
        self.imu_green = QIcon('./icons/imuVerde.svg')
        self.imu_red = QIcon('./icons/imuRojo.svg')
        self.imuBtn.setIcon(self.imu_red) 

        camera_good = "camera_good" + str(dron)
        self.cameraBtn = getattr(self.main, camera_good)
        self.camera_green = QIcon('./icons/cameraVerde.svg')
        self.camera_red = QIcon('./icons/cameraRojo.svg')
        self.cameraBtn.setIcon(self.camera_red) 
        
        frame_name = "frame_drone" + str(dron)
        frame = getattr(self.main,frame_name)
        frame.show()

    def camera_callback(self, data):
        height = data.height
        if height != "null":
            self.telemetria.set_salud_camara("Ok")
            self.cameraBtn.setIcon(self.camera_green)
        else:
            self.cameraBtn.setIcon(self.camera_red)
        
    def drone_data(self,data):
        salud_gyro = ""
        salud_acelerometro = ""
        salud_magnetometro = ""
        salud_presion = ""
        for item in data.status:

            if item.name == 'mavros: Heartbeat':
                    id = item.hardware_id
                    self.dron.set_hardware_id(id)

                    for v in item.values:
                        if v.key == 'Vehicle type':
                            self.dron.set_tipo(v.value)
                            self.telemetria.set_salud_controladora("Ok")

                        if v.key == 'Autopilot type':
                            self.dron.set_controladora(v.value)


            if item.name == "mavros: Battery":
                for value in item.values:
                    if value.key == "Voltage":
                        self.dron.set_voltaje_inicial(str(value.value))
                    if value.key == "Remaining":
                        porcentaje = value.value
                        self.telemetria.set_porcentaje_bateria(porcentaje)


            if item.name == "mavros: System":
                for value in item.values:
                    if value.key == "Battery":
                        if value.value == "Ok":
                            self.telemetria.set_salud_bateria(value.value)
                            self.batteryBtn.setIcon(self.battery_green)
                        else:
                            self.batteryBtn.setIcon(self.battery_red)
                    if value.key == "GPS":
                        if value.value == "Ok":
                            self.telemetria.set_salud_gps(value.value)
                            self.gpsBtn.setIcon(self.gps_green)
                        else:
                            self.gpsBtn.setIcon(self.gps_red)           
                    if value.key == "motor outputs / control":
                        if value.value == "Ok":
                            self.telemetria.set_salud_motores(value.value)
                            self.motorBtn.setIcon(self.motor_green)
                        else:
                            self.motorBtn.setIcon(self.motor_red)
                    if value.key == "rc receiver":
                        if value.value == "Ok":
                            self.autopilotBtn.setIcon(self.autopilot_green)
                        else:
                            self.autopilotBtn.setIcon(self.autopilot_red)
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
                        self.imuBtn.setIcon(self.imu_green)
                    else:
                        self.imuBtn.setIcon(self.imu_red)
        rospy.sleep(1)