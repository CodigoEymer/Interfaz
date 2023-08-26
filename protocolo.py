import rospy
from mavros_msgs.msg import  WaypointReached, ParamValue
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from mavros_msgs.srv import ParamSet
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import datetime as d
from config_module import config_module
import os

from diagnostic_msgs.msg import DiagnosticArray
from sensor_msgs.msg import CameraInfo
from Database.foto.foto import foto
from communication_module import communication_module
from Database.telemetria.telemetria import telemetria
from Database.dron.dron import dron
from Database.foto.foto import foto

class protocolo():
    def __init__(self,parent, telemetriaV,dronV,fotoV):
            self.parent = parent
            self.telemetriaV = telemetriaV
            self.dronV = dronV
            self.fotoV = fotoV
            self.ns_unicos = []
            self.n_drones = 0
            rospy.init_node('srvComand_node', anonymous=True)
            rospy.Subscriber("diagnostics", DiagnosticArray,self.drone_data)
                 
    def drone_data(self,data):

        ns = data.status[3].name
        ns = ns.split("/")
        ns = ns[0]

        if ns not in self.ns_unicos:
            telemetriaN = telemetria()
            dronN = dron()
            fotoN = foto()
            self.telemetriaV.append(telemetriaN)
            self.dronV.append(dronN)
            self.fotoV.append(fotoN)

            self.commu_module = communication_module(self.parent,self.telemetriaV[-1],self.dronV[-1],self.fotoV[-1],ns)
            self.ns_unicos.append(ns) 
            print("ns:",ns)
            self.n_drones = len(self.ns_unicos)    
        rospy.sleep(1)
        