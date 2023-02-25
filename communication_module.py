import rospkg

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from diagnostic_msgs.msg import DiagnosticArray


from mavros_msgs.srv import *

from std_msgs.msg import String
from mavros_msgs.srv import *

class communication_module():
    def __init__(self):
            rospy.init_node('srvComand_node', anonymous=True)
            rospy.Subscriber("diagnostics", DiagnosticArray,self.status_dron)

    def status_dron(self,data):
        for item in data.status:
                if item.name == 'mavros: Heartbeat':
                    for v in item.values:
                        if v.key == 'Vehicle type':
                            vehicle_type = v.value
                            print("Vehicle type:", vehicle_type)
                if item.name == 'mavros: Heartbeat':
                    for v in item.values:
                        if v.key == 'Autopilot type':
                            Autopilot_type = v.value
                            print("Autopilot type:", Autopilot_type)

                if item.name == "mavros: Battery":
                    for value in item.values:
                        if value.key == "Voltage":
                            voltage = float(value.value)
                            print("Voltage: {} V".format(voltage))