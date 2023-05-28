import rospy
from mavros_msgs.msg import  WaypointReached
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from mavros_msgs.srv import ParamSet
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem
import cv2
from config_module import config_module

class communication_module():

    Dron = ["null","null","null","null"]
    Posiciones =["null","null","null","null","null","null","null"]
  # Dron     = [id,tipo,controladora,voltaje]
  # Posiciones =[id,latitud,longitud,altitud, ginada,alabeo,cabeceo]

    def __init__(self, parent):
            self.main = parent
            self.counter=0
            rospy.init_node('srvComand_node', anonymous=True)
            rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, self.globalPositionCallback)
            rospy.Subscriber("/mavros/imu/data", Imu, self.imu_callback)
            rospy.Subscriber("/mavros/mission/reached", WaypointReached, self.waypoint_reached_callback)
            rospy.Subscriber("/mavros/camera/image_raw",  Image, self.image_callback)
            
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
        }
        for id, value in params_to_set.items():
            if not self.set_param(id, value):
                print("Falla al poner el parametro" %id)
        
    def set_param(self, id, value):
        rospy.wait_for_service('/mavros/param/set')
        try:
            set_param_srv = rospy.ServiceProxy('/mavros/param/set',ParamSet)
            resp = set_param_srv(id, value)
            return resp.success
        except rospy.ServiceException as e:
            print("Fallo al llamar el servicio: %$" %e)