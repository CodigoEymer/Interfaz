import rospy
from mavros_msgs.msg import  WaypointReached, ParamValue
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from mavros_msgs.srv import ParamSet
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from PyQt5.QtGui import QIcon
import cv2
import datetime as d
import os
import threading
from Database.foto.foto import foto

from diagnostic_msgs.msg import DiagnosticArray
from sensor_msgs.msg import CameraInfo

lock_fotos = threading.Lock()


class communication_module():

    flag_insertTelemetria = 1
    def __init__(self, parent,telemetria,dron,n_canal,ns,config, fotos):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the attributes of an object, which are sometimes called properties.
        These attributes are typically given as parameters to __init__.
        
        :param self: Represent the instance of the class
        :param parent: Associate the object with its parent window
        :param telemetria: Pass the telemetria data from the main window to this one
        :param dron: Access the drone's functions
        :param n_canal: Identify the channel in which the drone is connected
        :param ns: Pass the namespace of the drone to be able to connect with it
        :param config: Get the configuration of the program, which is stored in a json file
        :param fotos: Pass the fotos list to the class, so that it can be modified by any function in this class
        :return: The frame
        :doc-author: Trelent
        """
        
        self.config= config
        self.main = parent
        self.telemetria = telemetria
        self.v_telemetria = []
        self.fotos= fotos
        self.dron = dron
        self.ns = ns
        self.Posicion = ["null","null","null"]
        self.flag_insertTelemetria_c = n_canal
        self.main.iniciar_hilo2(self)
        self.c=0
        self.frame=None

    def topicos(self):
        """
        Suscribe el dron a varios topicos ROS para recibir informacion.

        Este metodo se encarga de configurar la suscripcion del dron a varios topicos ROS
        para recibir informacion importante de los siguientes topicos:
        
        - /<namespace>/mavros/camera/camera_info: Informacion de la camara.
        - /<namespace>/mavros/global_position/raw/fix: Posicion global.
        - /<namespace>/mavros/imu/data: Datos de la IMU (Unidad de Medicion Inercial).
        - /<namespace>/mavros/mission/reached: Notificacion de llegada a waypoints.
        - /<namespace>/mavros/camera/image_raw: Imagen capturada por la camara.

        Los callbacks correspondientes son definidos para procesar los datos recibidos.
        """
        
        rospy.Subscriber("/"+self.ns+"/mavros/camera/camera_info", CameraInfo, self.camera_callback)
        rospy.Subscriber("/"+self.ns+"/mavros/global_position/raw/fix", NavSatFix, self.globalPositionCallback)
        rospy.Subscriber("/"+self.ns+"/mavros/imu/data", Imu, self.imu_callback)
        rospy.Subscriber("/"+self.ns+"/mavros/mission/reached", WaypointReached, self.waypoint_reached_callback)
        rospy.Subscriber("/"+self.ns+"/mavros/camera/image_raw",  Image, self.image_callback)
        #self.main.drone_1.setIcon(QIcon('./icons/drone_ok.svg'))
            
            

    def create_folder(self, path):
        """
        The create_folder function creates a folder at the specified path.
        If the folder already exists, it does nothing. If there is an error creating
        the folder, it prints out an error message.
        
        :param self: Represent the instance of the object itself
        :param path: Specify the path of the folder that is to be created
        :return: Nothing
        :doc-author: Trelent
        """
        
        try:
            # If the folder does not exist, create it
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            print("An error occurred while creating folder: ", e)

    def waypoint_reached_callback(self, msg):
        """
        Callback para manejar la llegada a un punto de ruta (waypoint).

        Parametros:
        - msg: Mensaje que indica que se ha alcanzado un waypoint.

        Este metodo se encarga de realizar las siguientes acciones:
        1. Crea una carpeta para almacenar imagenes relacionadas con la mision del dron.
        2. Captura una imagen y la guarda en la carpeta mencionada.
        3. Crea un objeto 'photo' para almacenar informacion sobre la imagen capturada,
        incluyendo el ID del dron, la hora de captura, latitud, longitud y altitud.
        4. Agrega el objeto 'photo' a la lista de fotos.

        Nota: Este metodo depende de la disponibilidad de datos como la imagen capturada,
        la configuracion del dron y la telemetria. Asegurate de que estos datos esten disponibles
        antes de llamar a este metodo.
        """
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
        photo = foto()
        # TO DO: Agregar cordenadas y hora de captura
        photo.set_id_dron(self.dron.get_id_dron())
        photo.set_hora_captura(hora_captura)
        photo.set_latitud_captura(self.telemetria.get_latitud())
        photo.set_longitud_captura(self.telemetria.get_longitud())
        photo.set_altitud_captura(self.telemetria.get_altitud())
        with lock_fotos:
            self.fotos.append(photo)

    def image_callback(self, image):
        self.image = image
        
        
    def imu_callback(self,data):
        """
        The imu_callback function is a callback function that receives the data from the imu topic and stores it in variables.
            Args:
                self (object): The object of this class.
                data (Imu): The Imu message received from the imu topic.
        
        :param self: Represent the instance of the class
        :param data: Get the data from the imu sensor
        :return: The roll, pitch and yaw of the drone
        :doc-author: Trelent
        """
        
        roll = data.orientation.x
        pitch = data.orientation.y
        yaw = data.orientation.z
        self.telemetria.set_cabeceo(pitch)
        self.telemetria.set_guinada(yaw)
        self.telemetria.set_alabeo(roll)

    def globalPositionCallback(self,globalPositionCallback):
        """
        Callback para manejar la actualizacion de la posicion global del dron.

        Parametros:
        - globalPositionCallback: Objeto que contiene informacion de la posicion global del dron.

        Este metodo se encarga de procesar y actualizar la informacion de la posicion global
        del dron, incluyendo latitud, longitud, altitud y hora de actualizacion. Luego, actualiza
        los atributos correspondientes en la clase 'telemetria' y, si esta habilitado, almacena
        los datos de telemetria en un vector y los inserta en una base de datos despues de cierta
        cantidad de actualizaciones.
        """
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
        
        if(self.main.flag_telemetria==1):
            self.v_telemetria.append(self.telemetria)
            if(len(self.v_telemetria)>=10 and communication_module.flag_insertTelemetria == self.flag_insertTelemetria_c):
                self.config.insertar_telemetria(self.v_telemetria)
                self.v_telemetria = []
                communication_module.flag_insertTelemetria= communication_module.flag_insertTelemetria+1

    def setFlightParameters(self, parameters, altura):
        """
        Configura los parametros de vuelo del dron.

        Parametros:
        - parameters: Lista que contiene los valores de los parametros de vuelo, en el orden siguiente:
        - WPNAV_ACCEL: Aceleracion maxima permitida en cm/s^2.
        - WPNAV_SPEED: Velocidad maxima permitida en cm/s.
        - altura: Altura para el modo RTL (Return to Launch).

        Este metodo configura los parametros de vuelo del dron con los valores especificados,
        incluyendo la aceleracion maxima, velocidad maxima y altura para el modo RTL (Return to Launch).
        """
        params_to_set = {                  # Increment  Range    Units
            'WPNAV_ACCEL' : parameters[0], #   10       50-500   cm/s^2 
            'WPNAV_SPEED' : parameters[1], #   50       20-2000  cm/s
            'WPNAV_SPEED_DN': 300,          #   10       10-500  cm/s
            'RTL_ALT': altura,
            'RTL_ALT_FINAL': 0
        }
        for id, value in params_to_set.items():
            if not self.set_param(id, value):
                print("Falla al poner el parametro %s" %id)
        
    def set_param(self, id, value):
        """
        Configura un parametro especifico del dron.

        Parametros:
        - id: Nombre del parametro a configurar.
        - value: Valor del parametro.

        Este metodo utiliza el servicio ROS para configurar un parametro especifico
        del dron con el valor proporcionado.
        
        Servicios utilizados:
        - /<namespace>/mavros/param/set: Servicio utilizado para configurar parametros individuales del dron.
        """
        rospy.wait_for_service("/"+self.ns+"/mavros/param/set")
        try:
            set_param_srv = rospy.ServiceProxy("/"+self.ns+"/mavros/param/set",ParamSet)
            param_value = ParamValue()
            param_value.integer = int(value)
            resp = set_param_srv(id, param_value)
            return resp.success
        except rospy.ServiceException as e:
            print("Fallo al llamar el servicio: %s" %e)

        
    def frame_a_modificar(self, frame):
        self.frame = frame
        self.topicos()
        self.icons = self.initialize_icons()

    def initialize_icons(self):
        icons = {
            "batteryVerde": QIcon('./icons/batteryVerde.svg'),
            "batteryRojo": QIcon('./icons/batteryRojo.svg'),
            "gpsVerde": QIcon('./icons/gpsVerde.svg'),
            "gpsRojo": QIcon('./icons/gpsRojo.svg'),
            "motorVerde": QIcon('./icons/motorVerde.svg'),
            "motorRojo": QIcon('./icons/motorRojo.svg'),
            "cpuVerde": QIcon('./icons/cpuVerde.svg'),
            "cpuRojo": QIcon('./icons/cpuRojo.svg'),
            "imuVerde": QIcon('./icons/imuVerde.svg'),
            "imuRojo": QIcon('./icons/imuRojo.svg'),
            "cameraVerde": QIcon('./icons/cameraVerde.svg'),
            "cameraRojo": QIcon('./icons/cameraRojo.svg'),
        }
        return icons
    def camera_callback(self, data):
        height = data.height
        if height != "null": # Si la altura no es nula se interpreta que la camara esta funcionando correctamente y pasa el icono de la camara a verde, de lo contrario queda rojo
            self.telemetria.set_salud_camara("Ok")
            self.frame.cameraBtn.setIcon(QIcon(self.icons["cameraVerde"]))
        else:
            self.frame.cameraBtn.setIcon(QIcon(self.icons["cameraRojo"]))

        
    def drone_data(self,data):
        """ La funcion drone_data actualiza varios aspectos del estado del dron, incluyendo:

        Identificacion del hardware y tipo de dron.
        Tipo de controladora y estado de salud de la controladora.
        Voltaje inicial y porcentaje de bateria.
        Estado de la conexion.
        Salud de la bateria, GPS, motor, piloto automatico, giroscopio, magnetometro, acelerometro y sensor de presion.

        Para cada uno de estos estados, la funcion ajusta los iconos y textos de la interfaz de usuario para reflejar el estado actual del dron. """

        if self.frame != None:
            salud_gyro = ""
            salud_acelerometro = ""
            salud_magnetometro = ""
            salud_presion = ""
            
            self.dron.set_hardware_id(data.status[3].hardware_id)
            self.dron.set_tipo(data.status[3].values[2].value)

            tipoControladora = data.status[3].values[3].value
            self.dron.set_controladora(tipoControladora)
            if tipoControladora == 'ArduPilot':
                self.telemetria.set_salud_controladora("Ok")

            self.dron.set_voltaje_inicial(data.status[5].values[0].value)
            self.telemetria.set_porcentaje_bateria(data.status[5].values[2].value)
            estado_conexion = data.status[0].message
            self.frame.button_estado.setText(estado_conexion)
            self.c=self.c+1


            salud_bateria = data.status[4].values[17].value
            if salud_bateria == "Ok" and estado_conexion == 'connected':
                self.telemetria.set_salud_bateria(salud_bateria)
                self.frame.batteryBtn.setIcon(QIcon(self.icons["batteryVerde"]))
            else:
                self.frame.batteryBtn.setIcon(QIcon(self.icons["batteryRojo"]))


            salud_gps = data.status[4].values[7].value
            if salud_gps == "Ok" and estado_conexion == 'connected':
                self.telemetria.set_salud_gps(salud_gps)
                self.frame.gpsBtn.setIcon(self.icons["gpsVerde"])
            else:
                self.frame.gpsBtn.setIcon(QIcon(self.icons["gpsRojo"]))   

            salud_motor = data.status[4].values[13].value
            if salud_motor == "Ok" and estado_conexion == 'connected':
                self.telemetria.set_salud_motores(salud_motor)
                self.frame.motorBtn.setIcon(QIcon(self.icons["motorVerde"]))
            else:
                self.frame.motorBtn.setIcon(QIcon(self.icons["motorRojo"]))
            
            salud_auto = data.status[4].values[14].value
            if salud_auto == "Ok" and estado_conexion == 'connected':
                self.frame.autopilotBtn.setIcon(QIcon(self.icons["cpuVerde"]))
            else:
                self.frame.autopilotBtn.setIcon(QIcon(self.icons["cpuRojo"]))

            salud_gyro = data.status[4].values[3].value
            salud_magnetometro = data.status[4].values[5].value
            salud_acelerometro = data.status[4].values[4].value
            salud_presion = data.status[4].values[6].value

            if salud_gyro == "Ok" and salud_magnetometro == "Ok" and salud_acelerometro == "Ok" and salud_presion == "Ok" and estado_conexion == 'connected':
                self.telemetria.set_salud_imu("Ok")
                self.frame.imuBtn.setIcon(QIcon(self.icons["imuVerde"]))
            else:
                self.frame.imuBtn.setIcon(QIcon(self.icons["imuRojo"]))
                    