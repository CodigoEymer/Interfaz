import sys
import os
import io
import rospy
import rospkg
import resources_rc
import folium
import json

from Database.usuarios.usuarios_dao_imp import usuarios_dao_imp
import config_module

from folium.plugins import Draw
import geocoder
from std_msgs.msg import String
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

from mavros_msgs.srv import *

g = geocoder.ip('me')
m = folium.Map(location=(g.latlng),tiles='OpenStreetMap',zoom_start=15)

draw = Draw(export=True,    
		filename="my_data.geojson",
        draw_options={
          	'polyline':False,
		    'rectangle':False,
          	'circle':False,
          	'circlemarker':False})

import MySQLdb
DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

class MainWindow(QMainWindow):



	def __init__(self):

		super(MainWindow, self).__init__()
		loadUi('interface.ui', self)
		
		self.ingresarBtn.clicked.connect(self.settings_page)
		self.crearUsuarioBtn.clicked.connect(self.signup_page)
		self.registerBtn.clicked.connect(self.register_button)
		self.cancelRegisterBtn.clicked.connect(self.login_page)	
		self.settingsBtn.clicked.connect(self.settings_page)
		self.generarTrayectBtn.clicked.connect(self.gen_tray)
		#self.pushButton_20.clicked.connect(self.get_location)
		self.homeBtn.clicked.connect(self.home_page)
		self.connectionBtn.clicked.connect(self.connection_page)
		self.telemetryBtn.clicked.connect(self.telemetry_page_2)
		self.missionBtn.clicked.connect(self.mission_page)
		self.playBtn.clicked.connect(self.armar)
		self.reportBtn.clicked.connect(self.report_page)
		self.userBtn_2.clicked.connect(self.config_user_page)
		self.updateBtn.clicked.connect(self.main_window)
		self.cancelUpdateBtn.clicked.connect(self.main_window)
	


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
		
		user_name = self.user_name_login.toPlainText()
		connection = usuarios_dao_imp(conn)
		user_list = connection.get_all_users()
		
		for user in user_list:
			db_user = str(user.get_nombre_usuario())
			if db_user == user_name:
				self.main_window()
				self.switchPagesStacked.setCurrentWidget(self.ConfiPage)
				m.add_child(draw)
				data = io.BytesIO()
				m.save(data, close_file = False)
				self.webView.setHtml(data.getvalue().decode())
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
		coordenadas = self.coords_text.toPlainText()

		datos= config_module.config_module(ciudad, direccion, nombre_mision, nombre_rdi, descripcion, campo_de_vision, alt_maxima, vel_maxima, acc_maxima, sobrelapamiento, coordenadas)
		
		datos.insertar_mision()


	def home_page(self):
		self.switchPagesStacked.setCurrentWidget(self.homePage_3)

	def connection_page(self):
		self.stackedWidget_2.setCurrentWidget(self.page)

	def telemetry_page_2(self):
		self.stackedWidget_2.setCurrentWidget(self.page_2)

	def mission_page(self):
		self.switchPagesStacked.setCurrentWidget(self.missionPage)

	def report_page(self):
		self.switchPagesStacked.setCurrentWidget(self.reportPage)

	def armar(self):
		self.label_29.setText("comando armar enviado")

		rospy.wait_for_service('/mavros/set_mode')
		try:
			flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
			isModeChanged = flightModeService(custom_mode='STABILIZE') #return true or false
		except rospy.ServiceException, e:
			print "service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e

		rospy.wait_for_service('/mavros/cmd/arming')
		try:
			armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
			armService(True)
		except rospy.ServiceException, e:
			print "Service arm call failed: %s"%e

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
