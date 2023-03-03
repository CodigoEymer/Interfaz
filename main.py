import sys
import os
import io
import rospy
import rospkg
import resources_rc
import json

from Database.usuarios.usuarios_dao_imp import usuarios_dao_imp,usuarios,usuarios_dao
import config_module
import communication_module
import server

from std_msgs.msg import String
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebSockets, QtNetwork
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QFile, QThread, pyqtSignal

from mavros_msgs.srv import *
import time
import prueba
import MySQLdb
DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)


cont=1
coords= []
wp_recarga=[] 
area= []
id_usuario = ""

class MainWindow(QMainWindow):

	def __init__(self):

		super(MainWindow, self).__init__()
		loadUi('interface.ui', self)
		
		self.ingresarBtn.clicked.connect(self.user_validation)
		self.crearUsuarioBtn.clicked.connect(self.signup_page)
		self.registerBtn.clicked.connect(self.register_button)
		self.cancelRegisterBtn.clicked.connect(self.login_page)	
		self.homeBtn.clicked.connect(self.home_page)
		self.generarTrayectBtn.clicked.connect(self.gen_tray)
		self.iniciarTrayectBtn.clicked.connect(self.init_trayct)
		self.settingsBtn.clicked.connect(self.settings_page)
		self.connectionBtn.clicked.connect(self.connection_page)
		self.telemetryBtn.clicked.connect(self.telemetry_page_2)
		self.missionBtn.clicked.connect(self.mission_page)
		self.playBtn.clicked.connect(self.armar)
		self.pauseBtn.clicked.connect(self.pausingMission)
		self.reportBtn.clicked.connect(self.report_page)
		self.userBtn_2.clicked.connect(self.config_user_page)
		self.updateBtn.clicked.connect(self.main_window)
		self.cancelUpdateBtn.clicked.connect(self.main_window)
		self.stackedWidget.setCurrentWidget(self.signInWindowWidget)

		self.hide_all_status()
		self.hide_all_health()
		self.hide_all_frames()

	def main_window(self):
			self.stackedWidget.setCurrentWidget(self.mainWindowWidget)

	def signin_window(self):
			self.stackedWidget.setCurrentWidget(self.signInWindowWidget)

	def register_button(self):
		nombre = self.name_text.toPlainText()
		nombre_usuario = self.user_name_text.toPlainText()
		celular = self.phone_text.toPlainText()
		correo = self.email_text.toPlainText()

		connection = usuarios_dao_imp(conn)
		connection.insert_user(nombre, nombre_usuario, correo, celular)
		self.stackedWidget_3.setCurrentWidget(self.logInPage)

	def login_page(self):
			self.stackedWidget_3.setCurrentWidget(self.logInPage)

	def signup_page(self):
			self.stackedWidget_3.setCurrentWidget(self.signUpPage)

	def config_user_page(self):
		self.signin_window()
		self.stackedWidget_3.setCurrentWidget(self.userConfiPage)

	def settings_page(self):
		self.main_window()
		self.switchPagesStacked.setCurrentWidget(self.ConfiPage)
		self.hide_all_drones()
		file = QFile("map2.html")
		if file.open(QFile.ReadOnly | QFile.Text):
			html = str(file.readAll())
			self.webView.setHtml(html)	

		communication_module.communication_module()

	def startThread(self):
		self.thread = prueba.Worker()
		self.thread.dataLoaded.connect(self.setData)
		self.thread.start()

	def setData(self, data):
		for i, row in enumerate(data):
			for j, item in enumerate(row):
				self.tableWidget.setItem(i, j, QTableWidgetItem(item))

	def user_validation(self):
		global id_usuario
		user_name = self.user_name_login.toPlainText()
		connection = usuarios_dao_imp(conn)
		user_list = connection.get_all_users()
		
		for user in user_list:
			db_user = str(user.get_nombre_usuario())
			if db_user == user_name:
				id_usuario = str(user.get_id_usuario())
				self.main_window()
				self.settings_page()
				break
			else:
				self.error_label.setText("Usuario no encontrado")

	def gen_tray(self):
		ciudad = self.city_text.toPlainText()
		direccion = self.address_text.toPlainText()
		nombre_mision = self.mission_name_text.toPlainText()
		nombre_rdi = self.roi_name_text.toPlainText()
		descripcion = self.description_text.toPlainText()
		campo_de_vision = self.vision_field_text.toPlainText()
		alt_maxima = self.max_height_text.toPlainText()
		vel_maxima = self.max_speed_text.toPlainText()
		acc_maxima = self.max_acc_text.toPlainText()
		sobrelapamiento = self.overlap_text.toPlainText()


		datos= config_module.config_module(id_usuario, ciudad, direccion, nombre_mision, nombre_rdi, descripcion, campo_de_vision, alt_maxima, vel_maxima, acc_maxima, sobrelapamiento,coords,str(area),str(wp_recarga))
		
		datos.insertar_mision()
		datos.insertar_wp_region()
		datos.insertar_wp_recarga()

	def init_trayct(self):
		global cont
		if cont == 9:
			self.drone_9.show()
			cont=1
		if cont == 8: 
			self.drone_8x.show()
			cont=9
		if cont == 7: 
			self.drone_7x.show()
			cont=8
		if cont == 6: 
			self.drone_6.show()
			cont=7
		if cont == 5: 
			self.drone_5.show()
			cont=6
		if cont == 4: 
			self.drone_4.show()
			cont=5
		if cont == 3: 
			self.drone_3x.show()
			cont=4
		if cont == 2:
			self.drone_2.show()
			cont=3
		if cont == 1:
			self.drone_1x.show()
			cont=2
	def home_page(self):
		self.switchPagesStacked.setCurrentWidget(self.homePage_3)

		estados = communication_module.communication_module.Estados
		posiciones = communication_module.communication_module.Posiciones

		self.show_states(estados, 1)
		self.show_states(estados, 4)

		id= posiciones[0]
		latitud=posiciones[1]
		longitud=posiciones[2]
		altitud=posiciones[3]
		guinada=posiciones[4]
		alaveo=posiciones[5]
		cabeceo=posiciones[6]

		self.tableWidget.setItem(0,0,QTableWidgetItem(str(id)))
		self.tableWidget.setItem(0,1,QTableWidgetItem(str(latitud)))
		self.tableWidget.setItem(0,2,QTableWidgetItem(str(longitud)))
		self.tableWidget.setItem(0,3,QTableWidgetItem(str(altitud)))
		self.tableWidget.setItem(0,4,QTableWidgetItem(str(guinada)))
		self.tableWidget.setItem(0,5,QTableWidgetItem(str(alaveo)))
		self.tableWidget.setItem(0,6,QTableWidgetItem(str(cabeceo)))

	def show_states(self, estados, dron):

		frame_name = "frame_drone" + str(dron)
		frame = getattr(self,frame_name)
		frame.show()

		conectado_status = "conectado_status" + str(dron)
		conectado = getattr(self,conectado_status)
		conectado.show()
		
		battery_good = "battery_good" + str(dron)
		battery_green = getattr(self, battery_good)
		battery_bad = "battery_bad" + str(dron)
		battery_red = getattr(self, battery_bad)

		gps_good = "gps_good" + str(dron)
		gps_green = getattr(self, gps_good)
		gps_bad = "gps_bad" + str(dron)
		gps_red = getattr(self, gps_bad)

		motor_good = "motor_good" + str(dron)
		motor_green = getattr(self, motor_good)
		motor_bad = "motor_bad" + str(dron)
		motor_red = getattr(self, motor_bad)

		autopilot_good = "autopilot_good" + str(dron)
		autopilot_green = getattr(self, autopilot_good)
		autopilot_bad = "autopilot_bad" + str(dron)
		autopilot_red = getattr(self, autopilot_bad)

		imu_good = "imu_good" + str(dron)
		imu_green = getattr(self, imu_good)
		imu_bad = "imu_bad" + str(dron)
		imu_red = getattr(self, imu_bad)

		camera_good = "camera_good" + str(dron)
		camera_green = getattr(self, camera_good)
		camera_bad = "camera_bad" + str(dron)
		camera_red = getattr(self, camera_bad)

		if estados[1] == "Ok":
			battery_green.show()
		else:
			battery_red.show()

		if estados[2] == "Ok":
			gps_green.show()
		else:
			gps_red.show()

		if estados[3] == "Ok":
			motor_green.show()
		else:
			motor_red.show()

		if estados[4] == "Ok":
			autopilot_green.show()
		else:
			autopilot_red.show()

		if estados[5] == "Ok" and estados[6] == "Ok" and estados[7] == "Ok" and estados[8] == "Ok":
			imu_green.show()
		else:
			imu_red.show()

		if estados[9] == "Ok":
			camera_green.show()
		else:
			camera_red.show()
		

	def connection_page(self):
		self.stackedWidget_2.setCurrentWidget(self.page)

	def telemetry_page_2(self):
		self.stackedWidget_2.setCurrentWidget(self.page_2)

	def mission_page(self):
		self.switchPagesStacked.setCurrentWidget(self.missionPage)
		file = QFile("map2.html")
		if file.open(QFile.ReadOnly | QFile.Text):
			html = str(file.readAll())
			self.webView_2.setHtml(html)	

	def report_page(self):
		self.switchPagesStacked.setCurrentWidget(self.reportPage)

	def pausingMission(self):
		pass

	def armar(self):
		self.label_29.setText("comando armar enviado")

		rospy.wait_for_service('/mavros/set_mode')
		try:
			flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
			isModeChanged = flightModeService(custom_mode='STABILIZE') #return true or false
		except rospy.ServiceException as e:
			print ("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)

		rospy.wait_for_service('/mavros/cmd/arming')
		try:
			armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
			armService(True)
		except rospy.ServiceException as e:
			print ("Service arm call failed: %s"%e)

	def hide_all_drones(self):
		self.drone_1.hide()
		self.drone_1x.hide()
		self.drone_2.hide()
		self.drone_2x.hide()
		self.drone_3.hide()
		self.drone_3x.hide()
		self.drone_4.hide()
		self.drone_4x.hide()
		self.drone_5.hide()
		self.drone_5x.hide()
		self.drone_6.hide()
		self.drone_6x.hide()
		self.drone_7.hide()
		self.drone_7x.hide()
		self.drone_8.hide()
		self.drone_8x.hide()
		self.drone_9.hide()
		self.drone_9x.hide()

	def hide_all_status(self):
		self.conectado_status1.hide()
		self.armado_status1.hide()
		self.en_mision_status1.hide()
		self.error_status1.hide()

		self.conectado_status2.hide()
		self.armado_status2.hide()
		self.en_mision_status2.hide()
		self.error_status2.hide()

		self.conectado_status3.hide()
		self.armado_status3.hide()
		self.en_mision_status3.hide()
		self.error_status3.hide()

		self.conectado_status4.hide()
		self.armado_status4.hide()
		self.en_mision_status4.hide()
		self.error_status4.hide()

		self.conectado_status5.hide()
		self.armado_status5.hide()
		self.en_mision_status5.hide()
		self.error_status5.hide()

	def hide_all_frames(self):
		self.frame_drone1.hide()
		self.frame_drone2.hide()
		self.frame_drone3.hide()
		self.frame_drone4.hide()
		self.frame_drone5.hide()


	def hide_all_health(self):
		
		self.battery_good1.hide()
		self.battery_good2.hide()
		self.battery_good3.hide()
		self.battery_good4.hide()
		self.battery_good5.hide()	

		self.battery_bad1.hide()
		self.battery_bad2.hide()
		self.battery_bad3.hide()
		self.battery_bad4.hide()
		self.battery_bad5.hide()

		self.gps_good1.hide()
		self.gps_good2.hide()
		self.gps_good3.hide()
		self.gps_good4.hide()
		self.gps_good5.hide()

		self.gps_bad1.hide()
		self.gps_bad2.hide()
		self.gps_bad3.hide()
		self.gps_bad4.hide()
		self.gps_bad5.hide()

		self.motor_good1.hide()
		self.motor_good2.hide()
		self.motor_good3.hide()
		self.motor_good4.hide()
		self.motor_good5.hide()

		self.motor_bad1.hide()
		self.motor_bad2.hide()
		self.motor_bad3.hide()
		self.motor_bad4.hide()
		self.motor_bad5.hide()

		self.autopilot_good1.hide()
		self.autopilot_good2.hide()
		self.autopilot_good3.hide()
		self.autopilot_good4.hide()
		self.autopilot_good5.hide()

		self.autopilot_bad1.hide()
		self.autopilot_bad2.hide()
		self.autopilot_bad3.hide()
		self.autopilot_bad4.hide()
		self.autopilot_bad5.hide()

		self.imu_good1.hide()
		self.imu_good2.hide()
		self.imu_good3.hide()
		self.imu_good4.hide()
		self.imu_good5.hide()

		self.imu_bad1.hide()
		self.imu_bad2.hide()
		self.imu_bad3.hide()
		self.imu_bad4.hide()
		self.imu_bad5.hide()

		self.camera_good1.hide()
		self.camera_good2.hide()
		self.camera_good3.hide()
		self.camera_good4.hide()
		self.camera_good5.hide()

		self.camera_bad1.hide()
		self.camera_bad2.hide()
		self.camera_bad3.hide()
		self.camera_bad4.hide()
		self.camera_bad5.hide()


def on_message_received(message):
    coords_dict = json.loads(message)

    global coords
    global wp_recarga
    global area
    coords = coords_dict['wp_region'][0]
    wp_recarga = coords_dict['wp_recarga']
    area = coords_dict['area']

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    handler = server.WebSocketHandler()
    handler.message_received.connect(on_message_received)
    handler.server.listen(QtNetwork.QHostAddress.LocalHost, 8765)
    sys.exit(app.exec_())

