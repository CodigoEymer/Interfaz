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


from diagnostic_msgs.msg import DiagnosticArray
from sensor_msgs.msg import CameraInfo

class communication_module():

    Dron = ["udp","prueba","autopilot","21.5"]
    
    Posiciones =["null","null","null","null","null","null","null"]
  # Posiciones =[id,latitud,longitud,altitud, ginada,alabeo,cabeceo]

    def __init__(self, parent):
            self.main = parent
            self.counter=0
            rospy.init_node('srvComand_node', anonymous=True)
            rospy.Subscriber("diagnostics", DiagnosticArray,self.drone_data)
            rospy.Subscriber("/mavros/camera/camera_info", CameraInfo, self.camera_callback)
            rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, self.globalPositionCallback)
            rospy.Subscriber("/mavros/imu/data", Imu, self.imu_callback)
            rospy.Subscriber("/mavros/mission/reached", WaypointReached, self.waypoint_reached_callback)
            rospy.Subscriber("/mavros/camera/image_raw",  Image, self.image_callback)
            self.dron_info()
            self.main.drone_1.setIcon(QIcon('./icons/drone_ok.svg'))

    def waypoint_reached_callback(self, msg):
        print("Waypoint reached: %s" % msg.wp_seq)
        self.counter= self.counter+1
        try:
            # Convert your ROS Image message to OpenCV2
            cv2_img = CvBridge().imgmsg_to_cv2(self.image, "bgr8")
        except CvBridgeError as e:
            print(e)
        else:
            # Save your OpenCV2 image as a jpeg 
            cv2.imwrite("/home/dronespsi/Interfaz/Images/Mision/wp"+str(self.counter)+".jpeg", cv2_img)

        # TO DO: Agregar cordenadas y hora de captura

    def image_callback(self, image):
        self.image = image
        
        
    def imu_callback(self,data):
        roll = data.orientation.x
        pitch = data.orientation.y
        yaw = data.orientation.z
        self.Posiciones[4] = yaw
        self.Posiciones[5] = pitch
        self.Posiciones[6] = roll
        #rospy.loginfo("Roll: %f, Pitch: %f, Yaw: %f", roll, pitch, yaw)


    def globalPositionCallback(self,globalPositionCallback):
        latitude = globalPositionCallback.latitude
        longitude = globalPositionCallback.longitude
        altitude = globalPositionCallback.altitude
        self.Posiciones[1] = latitude
        self.Posiciones[2] = longitude
        self.Posiciones[3] = altitude
        for item in range(3):
            self.main.tableWidget.setItem(0, item+1, QTableWidgetItem(str(self.Posiciones[item+1])))
        self.main.tableWidget.repaint()

    def setFlightParameters(self, conf_module):
        parameters = conf_module.getParameters()
        params_to_set = {                  # Increment  Range    Units
            'WPNAV_ACCEL' : parameters[0], #   10       50-500   cm/s^2 
            'WPNAV_SPEED' : parameters[1], #   50       20-2000  cm/s
            'WPNAV_SPEED_DN': 300          #   10       10-500  cm/s
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
        self.Dron = ["null","null","null","null","null","null","null","null","null","null"]

        self.Estados = ["null","null","null","null","null","null","null","null","null","null"]
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
        self.Estados[9] = height
        if height != "null":
            self.cameraBtn.setIcon(self.camera_green)
        else:
            self.cameraBtn.setIcon(self.camera_red)
        
    def drone_data(self,data):
        for item in data.status:

            if item.name == 'mavros: Heartbeat':
                    id = item.hardware_id
                    self.Estados[0] = id
                    self.Dron[0] = id
                    self.Posiciones[0] = id

                    for v in item.values:
                        if v.key == 'Vehicle type':
                            tipo = v.value
                            self.Dron[1] = tipo

                        if v.key == 'Autopilot type':
                            controladora = v.value
                            self.Dron[2] = controladora


            if item.name == "mavros: Battery":
                if value.key == "Voltage":
                    voltage = value.value
                    self.Dron[3] = voltage
                if value.key == "Remaining":
                    porcentaje = value.value


            if item.name == "mavros: System":
                for value in item.values:
                    if value.key == "Battery":
                        self.Estados[1] = value.value
                        if value.value == "Ok":
                            self.batteryBtn.setIcon(self.battery_green)
                        else:
                            self.batteryBtn.setIcon(self.battery_red)
                    if value.key == "GPS":
                        self.Estados[2] = value.value
                        if value.value == "Ok":
                            self.gpsBtn.setIcon(self.gps_green)
                        else:
                            self.gpsBtn.setIcon(self.gps_red)           
                    if value.key == "motor outputs / control":
                        self.Estados[3] = value.value
                        if value.value == "Ok":
                            self.motorBtn.setIcon(self.motor_green)
                        else:
                            self.motorBtn.setIcon(self.motor_red)
                    if value.key == "rc receiver":
                        self.Estados[4] = value.value
                        if value.value == "Ok":
                            self.autopilotBtn.setIcon(self.autopilot_green)
                        else:
                            self.autopilotBtn.setIcon(self.autopilot_red)
                    if value.key == "3D gyro":
                        self.Estados[5] = value.value
                    if value.key == "3D magnetometer":
                        magnetometro = value.value
                        self.Estados[6] = magnetometro
                    if value.key == "3D accelerometer":
                        acelerometro = value.value
                        self.Estados[7] = acelerometro
                    if value.key == "absolute pressure":
                        presion = value.value
                        self.Estados[8] = presion

                    if self.Estados[5] == "Ok" and self.Estados[6] == "Ok" and self.Estados[7] == "Ok" and self.Estados[8] == "Ok":
                        self.imuBtn.setIcon(self.imu_green)
                    else:
                        self.imuBtn.setIcon(self.imu_red)