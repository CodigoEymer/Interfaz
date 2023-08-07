import rospy
from diagnostic_msgs.msg import DiagnosticArray
from sensor_msgs.msg import CameraInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem

class dron_info():
    
      # Estados   = [id,bateria,gps,motor,rc_receiver,giroscopio, magnetometro,acelerometro,presion,camara]
    def __init__(self, parent):
        # Dron     = [id_mision,ac_max,vel_max,alt_max,cvH,cvV,controladora,voltaje_inicial,tipo,hardware_id]
        self.Dron = ["null","null","null","null","null","null","null","null","null","null"]

        self.Estados = ["null","null","null","null","null","null","null","null","null","null"]
        self.main = parent
        dron=1
        rospy.Subscriber("diagnostics", DiagnosticArray,self.drone_data)
        rospy.Subscriber("/dron1/mavros/camera/camera_info", CameraInfo, self.camera_callback)
        
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
                    print("Nivel de porcentaje de la bateria:", porcentaje)


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

       
		