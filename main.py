import sys
import os
import io
import rospy
import rospkg
import resources_rc
import json

from Database.usuarios.usuarios_dao_imp import usuarios_dao_imp,usuarios,usuarios_dao
import config_module
import server

import geocoder
from std_msgs.msg import String
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebSockets, QtNetwork
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QFile

from mavros_msgs.srv import *

g = geocoder.ip('me')

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
		if cont == 8: 
			self.drone_8.show()
			cont=9
		if cont == 7: 
			self.drone_7.show()
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
			self.drone_3.show()
			cont=4
		if cont == 2:
			self.drone_2.show()
			cont=3
		if cont == 1:
			self.drone_1x.show()
			cont=2
	def home_page(self):
		self.switchPagesStacked.setCurrentWidget(self.homePage_3)
		self.frame_15.hide()

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
		#self.drone_2x.hide()
		self.drone_3.hide()
		self.drone_4.hide()
		self.drone_5.hide()
		self.drone_6.hide()
		self.drone_7.hide()
		self.drone_8.hide()
		self.drone_9.hide()

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

