import sys
import os
import io
import rospy
import rospkg
import resources_rc
import json
import datetime

from Database.usuarios.usuarios_dao_imp import usuarios_dao_imp,usuarios,usuarios_dao
from Database.mision.mision_dao_imp import mision_dao_imp
from Database.wp_dron.wp_dron import wp_dron
import config_module
import communication_module
import server
import Cobertura

from std_msgs.msg import String
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebSockets, QtNetwork
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QFile, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot

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


coords= []
wp_recarga=[] 
area= []
id_usuario = ""
db_user_id=""
db_user_list=[]



class MainWindow(QMainWindow):

	def __init__(self):

		super(MainWindow, self).__init__()
		loadUi('interface.ui', self)
		
		self.lista_wp = []

		self.ingresarBtn.clicked.connect(self.user_validation)
		self.user_name_login.returnPressed.connect(self.user_validation)
		self.crearUsuarioBtn.clicked.connect(self.signup_page)
		self.registerBtn.clicked.connect(self.register_button)
		self.cancelRegisterBtn.clicked.connect(self.login_page)	
		self.homeBtn.clicked.connect(self.home_page)
		self.generarTrayectBtn.clicked.connect(self.gen_tray)
		self.iniciarTrayectBtn.clicked.connect(self.init_trayct)
		self.drone_1.clicked.connect(self.disconnect_socket)
		self.settingsBtn.clicked.connect(self.settings_page)
		self.missionBtn.clicked.connect(self.mission_page)
		self.playBtn.clicked.connect(self.armar)
		self.pauseBtn.clicked.connect(self.pausingMission)
		self.reportBtn.clicked.connect(self.report_page)
		self.city_btn.clicked.connect(self.city_btn_function)
		self.mission_name_btn.clicked.connect(self.mission_name_btn_function)
		self.user_name_btn.clicked.connect(self.user_name_btn_function)
		self.date_btn.clicked.connect(self.date_btn_function)
		self.generate_report.clicked.connect(self.report_function)
		self.userBtn_2.clicked.connect(self.config_user_page)
		self.updateBtn.clicked.connect(self.main_window)
		self.cancelUpdateBtn.clicked.connect(self.main_window)
		self.stackedWidget.setCurrentWidget(self.signInWindowWidget)
		

		self.hide_all_frames()

	def set_default_icons(self):

		default = "background-color: rgb(203, 218, 216);"

		self.settingsBtn.setIcon(QIcon('./icons/IconoConfiAzul.svg'))
		self.settingsBtn.setStyleSheet(default)

		self.homeBtn.setIcon(QIcon('./icons/IconoHomeAzul.svg'))
		self.homeBtn.setStyleSheet(default)

		self.missionBtn.setIcon(QIcon('./icons/IconoMisionAzul.svg'))
		self.missionBtn.setStyleSheet(default)

		self.reportBtn.setIcon(QIcon('./icons/IconoReporteAzul.svg'))
		self.reportBtn.setStyleSheet(default)


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
		self.set_default_icons()
		icon = QIcon('./icons/IconoConfiGris.svg')
		self.settingsBtn.setIcon(icon)
		self.settingsBtn.setStyleSheet("background-color: rgb(3, 33, 77)")
		
		self.main_window()
		self.switchPagesStacked.setCurrentWidget(self.ConfiPage)
		
		file = QFile("map2.html")
		if file.open(QFile.ReadOnly | QFile.Text):
			html = str(file.readAll())
			self.webView.setHtml(html)

		communication_module.communication_module()
		self.startThread()

	def startThread(self):
		self.thread = prueba.Worker()
		self.thread.dataLoaded.connect(self.setData)
		self.thread.start()

	def setData(self, data):
		self.drone_1.setIcon(QIcon('./icons/drone_ok.svg'))
		for j, item in enumerate(data):
			self.tableWidget.setItem(0, j, QTableWidgetItem(str(item)))

	def user_validation(self):
		global id_usuario
		user_name = self.user_name_login.text()
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
		ciudad = self.city_text.text()
		direccion = self.address_text.text()
		nombre_mision = self.mission_name_text.text()
		nombre_rdi = self.roi_name_text.text()
		descripcion = self.description_text.text()
		campo_de_vision = self.vision_field_text.text()
		alt_maxima = self.max_height_text.text()
		vel_maxima = self.max_speed_text.text()
		acc_maxima = self.max_acc_text.text()
		sobrelapamiento = self.overlap_text.text()

		controladora = communication_module.communication_module.Dron[2]
		votaje_bateria = communication_module.communication_module.Dron[3]
		tipo = communication_module.communication_module.Dron[1]

		datos= config_module.config_module(id_usuario, ciudad, direccion, nombre_mision, nombre_rdi, descripcion, campo_de_vision, alt_maxima, vel_maxima, acc_maxima, sobrelapamiento,coords,str(area),str(wp_recarga),controladora,str(votaje_bateria),tipo)
		
		datos.insertar_mision()
		datos.insertar_wp_region()
		datos.insertar_wp_recarga()
		datos.insertar_dron()
		Vwp = coords
		h_max = self.max_height_text.text()


		Trayectorias = datos.generar_trayectoria()

		self.lista_wp = Trayectorias.ciclos()
		wp_retorno_aut = Trayectorias.calcular_wp_retorno(0.25)


		for item in self.lista_wp:
			handler.broadcast(str(item))
			print("wp:"+str(item))
		
		handler.broadcast("last")
		for item2 in wp_retorno_aut:
			handler.broadcast(str(item2))
			print("retorno:"+str(item2))
		datos.insertar_wp_dron(self.lista_wp,h_max)
		
	def init_trayct(self):
		self.switchPagesStacked.setCurrentWidget(self.missionPage)
		Cobertura.StartMission(self.lista_wp,self.progressBar_4)
		
		pass

	def disconnect_socket(self):
		handler.on_disconnected()

	def home_page(self):
		self.set_default_icons()
		icon = QIcon('./icons/IconoHomeGris.svg')
		self.homeBtn.setIcon(icon)
		self.homeBtn.setStyleSheet("background-color: rgb(3, 33, 77)")
		self.switchPagesStacked.setCurrentWidget(self.homePage_3)
		estados = communication_module.communication_module.Estados
		self.show_states(estados, 1)

	def show_states(self, estados, dron):

		frame_name = "frame_drone" + str(dron)
		frame = getattr(self,frame_name)
		frame.show()

		conectado_status = "conectado_status" + str(dron)
		conectado = getattr(self,conectado_status)
		conectado.setText("Conectado")
		
		battery = "battery_good" + str(dron)
		batteryBtn = getattr(self, battery)
		battery_green = QIcon('./icons/batteryVerde.svg')
		battery_red = QIcon('./icons/batteryRojo.svg')


		gps_good = "gps_good" + str(dron)
		gpsBtn = getattr(self, gps_good)
		gps_green = QIcon('./icons/gpsVerde.svg')
		gps_red = QIcon('./icons/gpsRojo.svg')

		motor_good = "motor_good" + str(dron)
		motorBtn = getattr(self, motor_good)
		motor_green = QIcon('./icons/motorVerde.svg')
		motor_red = QIcon('./icons/motorRojo.svg')

		autopilot_good = "autopilot_good" + str(dron)
		autopilotBtn = getattr(self, autopilot_good)
		autopilot_green = QIcon('./icons/cpuVerde.svg')
		autopilot_red = QIcon('./icons/cpuRojo.svg')


		imu_good = "imu_good" + str(dron)
		imuBtn = getattr(self, imu_good)
		imu_green = QIcon('./icons/imuVerde.svg')
		imu_red = QIcon('./icons/imuRojo.svg')

		camera_good = "camera_good" + str(dron)
		cameraBtn = getattr(self, camera_good)
		camera_green = QIcon('./icons/cameraVerde.svg')
		camera_red = QIcon('./icons/cameraRojo.svg')

		if estados[1] == "Ok":
			batteryBtn.setIcon(battery_green)
		else:
			batteryBtn.setIcon(battery_red)

		if estados[2] == "Ok":
			gpsBtn.setIcon(gps_green)
		else:
			gpsBtn.setIcon(gps_red)

		if estados[3] == "Ok":
			motorBtn.setIcon(motor_green)
		else:
			motorBtn.setIcon(motor_red)

		if estados[4] == "Ok":
			autopilotBtn.setIcon(autopilot_green)
		else:
			autopilotBtn.setIcon(autopilot_red)

		if estados[5] == "Ok" and estados[6] == "Ok" and estados[7] == "Ok" and estados[8] == "Ok":
			imuBtn.setIcon(imu_green)
		else:
			imuBtn.setIcon(imu_red)

		if estados[9] == "Ok":
			cameraBtn.setIcon(camera_green)
		else:
			cameraBtn.setIcon(camera_red)
		


	def mission_page(self):
		self.set_default_icons()
		icon = QIcon('./icons/IconoMisionGris.svg')
		self.missionBtn.setIcon(icon)
		self.missionBtn.setStyleSheet("background-color: rgb(3, 33, 77)")

		self.switchPagesStacked.setCurrentWidget(self.missionPage)
		file = QFile("map2.html")
		if file.open(QFile.ReadOnly | QFile.Text):
			html = str(file.readAll())
			self.webView_2.setHtml(html)	

	def report_page(self):
		self.set_default_icons()
		icon = QIcon('./icons/IconoReporteGris.svg')
		self.reportBtn.setIcon(icon)
		self.reportBtn.setStyleSheet("background-color: rgb(3, 33, 77)")
		self.switchPagesStacked.setCurrentWidget(self.reportPage)
		self.stackedWidget_2.setCurrentWidget(self.filers_widget)
		
		# self.date_frame.hide()
		# self.city_frame.hide()
		# self.mission_frame.hide()

	def user_name_btn_function(self):
		self.user_options.clear()
		global db_users_list
		db_users_list= self.search_users()
		self.user_options.addItem("Select")
		for element in db_users_list:
			self.user_options.addItem(element)
		self.user_options.currentIndexChanged.connect(self.username_selected)

	def search_users(self):
		global db_user_list
		nameUsers= []
		user_conect = usuarios_dao_imp(conn)
		db_user_list = user_conect.get_all_users()
		for user in db_user_list:
			nameUsers.append(user.get_nombre_usuario()) 
		
		nameUsers = set(nameUsers)

		return nameUsers

	def search_user_id(self):
		global db_user_id
		userSelect=self.selected_username.text()
		for user in db_user_list:
			db_user = str(user.get_nombre_usuario())
			if db_user == userSelect:
				db_user_id = str(user.get_id_usuario())
				break
			else:
				self.error_label.setText("Usuario no encontrado")

	
	@pyqtSlot(int)
	def username_selected(self):
		select_item = self.user_options.currentText()
		self.selected_username.setText(select_item)
		self.search_user_id()

	def city_btn_function(self):
		self.city_options.clear()
		db_list= self.search_cities()
		self.city_options.addItem("Select")
		for element in db_list:
			self.city_options.addItem(element)
		self.city_options.currentIndexChanged.connect(self.city_selected)

	@pyqtSlot(int)
	def city_selected(self):
		select_item = self.city_options.currentText()
		self.selected_city.setText(select_item)

	def search_cities(self):
		mision_connect = mision_dao_imp(conn)
		misions = mision_connect.get_all_missions_xUser(db_user_id)
		ciudades = []

		for mision in misions:
			ciudades.append(mision.get_ciudad()) 
		return set(ciudades)

	def mission_name_btn_function(self):
		db_list=self.search_mission_names()
		self.missionname_options.clear()
		self.missionname_options.addItem("Select")
		for element in db_list:
			self.missionname_options.addItem(element)
		self.missionname_options.currentIndexChanged.connect(self.mission_selected)

	@pyqtSlot(int)
	def mission_selected(self):
		select_item = self.missionname_options.currentText()
		self.selected_mission.setText(select_item)

	def search_mission_names(self):
		cytySelect = self.selected_city.text()
		mision_connect = mision_dao_imp(conn)
		misions = mision_connect.get_all_missions_xUserANDciudad(db_user_id, cytySelect)
		name_misions =[]
		for mision in misions:
			name_misions.append(mision.get_nombre_mision()) 
		return set(name_misions)

	def search_dates(self):
		cytySelect = self.selected_city.text()
		name_mision = self.selected_mission.text()
		dates= []
		date_conect = mision_dao_imp(conn)
		db_dates_list = date_conect.get_all_missions_xUserANDciudadANDname(db_user_id,cytySelect,name_mision)
		for date in db_dates_list:
			dates.append(str(date.get_fecha())+" "+date.get_hora_inicio())	
		dates = set(dates)

		return dates

	def date_btn_function(self):
		self.date_options.clear()
		db_list = self.search_dates()
		self.date_options.addItem("Select")
		for element in db_list:
			self.date_options.addItem(element)
		self.date_options.currentIndexChanged.connect(self.date_selected)

	@pyqtSlot(int)
	def date_selected(self):
		select_item = self.date_options.currentText()
		self.selected_date.setText(select_item)
		
	def report_function(self):
		user_load = usuarios_dao_imp(conn)
		usuario = user_load.get_user(db_user_id)
		self.label_36.setText(usuario.get_nombre())
		self.label_37.setText(usuario.get_correo())
		self.label_38.setText(usuario.get_celular())

		dateTimeList = self.selected_date.text().split()
		mision_load = mision_dao_imp(conn)
		mision = mision_load.get_mission(dateTimeList[0],dateTimeList[1])

		self.label_47.setText(mision.get_nombre_mision())
		self.label_48.setText(mision.get_ciudad())
		self.label_49.setText(mision.get_nombre_ubicacion())
		self.label_50.setText(mision.get_descripcion())
		self.label_51.setText(str(mision.get_dimension())+" m2")
		self.label_52.setText("TO DO")
		self.label_53.setText("TO DO")
		self.label_55.setText(str(mision.get_fecha()))

		self.stackedWidget_2.setCurrentWidget(self.report_view_widget)


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


	def hide_all_frames(self):
		self.frame_drone1.hide()
		self.frame_drone2.hide()
		self.frame_drone3.hide()
		self.frame_drone4.hide()
		self.frame_drone5.hide()


def on_message_received(message):
    coords_dict = json.loads(message)

    global coords
    global wp_recarga
    global area
    coords = coords_dict['wp_region'][0]
    coords.pop()
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

