import rospkg

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from diagnostic_msgs.msg import DiagnosticArray
import main


from mavros_msgs.srv import *

from std_msgs.msg import String
from mavros_msgs.srv import *

class communication_module():

    Estados = ["null","null","null","null","null","null","null","null","null","null"]
    Dron = ["null","null","null","null"]
    Posiciones =["null","null","null","null","null","null","null"]
  # Dron     = [id,tipo,controladora,voltaje]
  # Estados   = [id,bateria,gps,motor,rc_receiver,giroscopio, magnetometro,acelerometro,presion,camara]
  # Posiciones =[id,latitud,longitud,altitud, ginada,alabeo,cabeceo]

    def __init__(self):
            rospy.init_node('srvComand_node', anonymous=True)
            rospy.Subscriber("diagnostics", DiagnosticArray,self.status_dron)
            rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, self.globalPositionCallback)
            rospy.Subscriber("/mavros/imu/data", Imu, self.imu_callback)

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
        #print ("longitude: %.7f" %longitude)
        #print ("latitude: %.7f" %latitude)
        self.Posiciones[1] = latitude
        self.Posiciones[2] = longitude
        self.Posiciones[3] = altitude


    def status_dron(self,data):
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
                    for value in item.values:
                        if value.key == "Voltage":
                            voltage = float(value.value)
                            self.Dron[3] = voltage
                            

                if item.name == "mavros: System":
                    for value in item.values:
                        if value.key == "Battery":
                            bateria = value.value 
                            self.Estados[1] = bateria

                        if value.key == "GPS":
                            gps = value.value
                            self.Estados[2] = gps           

                        if value.key == "motor outputs / control":
                            motor = value.value
                            self.Estados[3] = motor

                        if value.key == "rc receiver":
                            rc_receiver = value.value
                            self.Estados[4] = rc_receiver

                        if value.key == "3D gyro":
                            giroscopio = value.value
                            self.Estados[5] = giroscopio

                        if value.key == "3D magnetometer":
                            magnetometro = value.value
                            self.Estados[6] = magnetometro

                        if value.key == "3D accelerometer":
                            acelerometro = value.value
                            self.Estados[7] = acelerometro

                        if value.key == "absolute pressure":
                            presion = value.value
                            self.Estados[8] = presion


        # for  dron in self.Dron:
        #     print(dron)
        # print("\n")
        # for  estado in self.Estados:
        #     print(estado)
        # print("\n")
        # for  posicion in self.Posiciones:
        #     print(posicion)
        # print("\n")
                              

                    