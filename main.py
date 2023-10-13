import sys
import os
import io
import rospy
import rospkg
import resources_rc
import json
import datetime
import Htelemetria
import hilo_componente_mision
import hilo_componente_estados
from Database.usuarios.usuarios_dao_imp import usuarios_dao_imp,usuarios
from Database.usuarios.usuarios import usuarios

from Database.wp_dron.wp_dron import wp_dron
#from Database.telemetria.telemetria import telemetria

from Database.mision.mision_dao_imp import mision_dao_imp
from Database.mision.mision import mision

from Database.wp_recarga.wp_recarga import wp_recarga as wp_recarga_obj
#from Database.dron.dron import dron
#from Database.foto.foto import foto
import config_module
from Trayectorias import Trayectorias
from sensores import CustomFrames
from custom_widget import CustomFrame
from protocolo import protocolo
from gestion import Gestion
from user_settings import SecondWindow
from mision_finalizada import MisionEndWindow
import server
import Cobertura
from PyQt5 import QtNetwork, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication,  QVBoxLayout, QGridLayout, QTableWidgetItem, QLabel, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import QFile, QEvent, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer

from mavros_msgs.srv import *
import time
import MySQLdb
import json
import threading


DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

coords= []
wp_recarga=[] 
area= []
db_user_list=[]

#telemetria = telemetria()
#dron = dron()

telemetriaV = []
dronV = []
fotoV = []

colors=[
          "#8A00AD",
          "#06AD00",
          "#0000FF",
          "#FF00FF",
          "#FFFF00",
          "#00FFFF"
        ]
current_usuario = usuarios()
current_mision = mision()
current_wp_recarga = wp_recarga_obj()
#foto = foto()
lock_progress_bar = threading.Lock()
lock_console = threading.Lock()

class MainWindow(QMainWindow):

	def __init__(self):
		
		self.flag_telemetria = 0
		self.wp_tramos = None
		self.cobertura = None
		self.config = config_module.config_module(None) 
		self.contador = 0
		super(MainWindow, self).__init__()
		loadUi('interface.ui', self)
		self.second_window = None
		self.finish_mission = None
		self.fotos=[]
		self.c=0
		self.n_cober = 0
		self.commu_objeto = []
		self.ingresarBtn.clicked.connect(self.user_validation)
		self.user_name_login.returnPressed.connect(self.user_validation)
		self.crearUsuarioBtn.clicked.connect(self.signup_page)
		self.registerBtn.clicked.connect(self.register_button)
		self.cancelRegisterBtn.clicked.connect(self.login_page)	
		self.homeBtn.clicked.connect(self.home_page)
		self.set_rate.clicked.connect(self.set_rate_hz)
		self.generarTrayectBtn.clicked.connect(self.gen_tray)
		self.iniciarTrayectBtn.clicked.connect(self.init_trayct)
		self.drone_1.clicked.connect(self.disconnect_socket)
		self.settingsBtn.clicked.connect(self.settings_page)
		self.missionBtn.clicked.connect(self.mission_page)
		self.reportBtn.clicked.connect(self.report_page)
		self.city_btn.clicked.connect(self.city_btn_function)
		self.mission_name_btn.clicked.connect(self.mission_name_btn_function)
		self.user_name_btn.clicked.connect(self.user_name_btn_function)
		self.date_btn.clicked.connect(self.date_btn_function)
		self.generate_report.clicked.connect(self.report_function)
		self.stopBtn.clicked.connect(self.stop_mision)		
		self.userBtn_2.clicked.connect(self.config_user_page)
		self.updateBtn.clicked.connect(self.update_user_data_up)
		self.cancelUpdateBtn.clicked.connect(self.main_window)
		self.stackedWidget.setCurrentWidget(self.signInWindowWidget)
		self.layout = QVBoxLayout()
		self.scrollAreaWidgetContents.setLayout(self.layout)
		self.layouts = QVBoxLayout()
		self.frame_13.setLayout(self.layouts)
		self.Qconsole.setReadOnly(True)
		self.buffer = []
		self.timer = QTimer()
		self.timer.timeout.connect(self.flush_buffer)
		self.timer.start(1000)  # Flush the buffer every 1 second
		#self.commu_module = communication_module(self,telemetria,dron, foto)
		
		self.file = QFile("mapa.html")
		if self.file.open(QFile.ReadOnly | QFile.Text):
			self.html = str(self.file.readAll())
			self.webView.setHtml(self.html)

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

	def update_user_data_up(self):
		id_user_actual = int(self.user.get_id_usuario())
		nombre = self.textEdit_7.toPlainText()
		nombre_usuario = self.textEdit_6.toPlainText()
		celular = self.textEdit_8.toPlainText()
		correo = self.textEdit_9.toPlainText()
		connection = usuarios_dao_imp(conn)
		try:
			connection.update_user(id_user_actual, str(nombre), str(nombre_usuario), str(correo), str(celular))
			#self.error_label.setText("Usuario Actualizado")
			self.user.set_nombre(str(nombre))
			self.user.set_nombre_usuario(str(nombre_usuario))
			self.user.set_celular(str(celular))
			self.user.set_correo(str(correo))

		except MySQLdb._exceptions.IntegrityError as e:
			self.user_feedback.setStyleSheet("color: red;")
		
		self.main_window()

	def set_rate_hz(self):
		rate = rospy.Rate(float(self.node_rate.text()))
		self.protocolo.modify_rate(rate)
  
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
		
		try:
			connection.insert_user(nombre, nombre_usuario, correo, celular)			
			self.login_page()
			self.error_label.setStyleSheet("color: green;")
			self.error_label.setText("Registro exitoso")

		except MySQLdb._exceptions.IntegrityError as e:
			self.user_feedback.setStyleSheet("color: red;")
			self.user_feedback.setText("Nombre de usuario ya existe")
		

	def login_page(self):
		self.error_label.clear()
		self.stackedWidget_3.setCurrentWidget(self.logInPage)

	def signup_page(self):
		self.user_feedback.clear()
		self.stackedWidget_3.setCurrentWidget(self.signUpPage)

	def config_user_page(self):
		if self.second_window is None:
			self.second_window = SecondWindow(self)
		self.second_window.exec_()
	
	def update_user_data(self):
		self.signin_window()
		self.stackedWidget_3.setCurrentWidget(self.userConfiPage)
		self.second_window.close()
		self.textEdit_6.setText(self.user.get_nombre_usuario())
		self.textEdit_7.setText(self.user.get_nombre())
		self.textEdit_8.setText(self.user.get_celular())
		self.textEdit_9.setText(self.user.get_correo())

	def logout(self):
		self.signin_window()
		self.stackedWidget_3.setCurrentWidget(self.logInPage)
		self.user_name_login.clear()
		self.second_window.close()

	def settings_page(self):
		self.set_default_icons()
		icon = QIcon('./icons/IconoConfiGris.svg')
		self.settingsBtn.setIcon(icon)
		self.settingsBtn.setStyleSheet("background-color: rgb(3, 33, 77)")
		
		self.main_window()
		self.switchPagesStacked.setCurrentWidget(self.ConfiPage)
		self.stackedWidget_4.setCurrentWidget(self.page)
		self.stackedWidget_5.setCurrentWidget(self.page_4)

		
		
	def user_validation(self):
		user_name = self.user_name_login.text()
		request = usuarios_dao_imp(conn)
		user_list = request.get_all_users()
		
		for user in user_list:
			db_user_name = str(user.get_nombre_usuario())
			if db_user_name == user_name:
				self.user = user
				self.main_window()
				self.home_page()
				rospy.init_node('srvComand_node', anonymous=True)
				self.rate = rospy.Rate(2)
				self.protocolo = protocolo(self,telemetriaV,dronV, fotoV, self.fotos, self.rate)
				self.error_label.setText("")
				break
			else:
				self.error_label.setText("Usuario no registrado, por favor registrese")

	def gen_tray(self):
		self.n_drones = self.protocolo.n_drones
		######
		self.city_text.setText("Cali")
		self.address_text.setText("calle 13, carrera 100")
		self.mission_name_text.setText("mision de prueba")
		self.roi_name_text.setText("Campus Univalle")
		self.description_text.setText("sobrevolando canchas")
		self.vision_field_text.setText("114.492")
		self.vision_field_text_2.setText("98.7566")
		self.max_height_text.setText("10")
		self.max_speed_text.setText("5")
		self.max_acc_text.setText("100")
		self.overlap_text.setText("1")
		######
		overlap = self.overlap_text.text()
		current_mision.set_ciudad(self.city_text.text())
		current_mision.set_direccion(self.address_text.text())
		current_mision.set_nombre_mision(self.mission_name_text.text())	
		current_mision.set_nombre_ubicacion(self.roi_name_text.text())
		current_mision.set_descripcion(self.description_text.text())
		current_mision.set_sobrelapamiento(overlap)

		self.gestion = Gestion(dronV)
		max_acce = self.max_acc_text.text()
		max_speed = self.max_speed_text.text()
		max_height = self.max_height_text.text()
		cvh = self.vision_field_text.text()
		cvv = self.vision_field_text_2.text()
		self.gestion.set_user_values(max_acce,max_speed,max_height,cvh,cvv)

		# peso = self.peso_text.text()
		# factor_seguridad = self.factor_seguridad_text.text()
		# seguridad = self.seguridad_text.text()
		# capacidad_b = self.capacidadB_text.text()
		# Voltaje_b = self.voltajeB_text.text()
		# potenciaKg = self.potenciaXkig_text.text()

		######
		peso = 2.11
		factor_seguridad = 1.5
		seguridad = 0.7
		capacidad_b = 6000
		Voltaje_b = 22.8
		potenciaKg = 275.3
		######
		current_mision.set_dimension(str(area))
		current_wp_recarga.set_wp(str(wp_recarga))
		self.config= config_module.config_module(str(self.user.get_id_usuario()),coords,current_wp_recarga,current_mision)
		
		self.config.insertar_mision()
		self.config.insertar_wp_region()
		self.config.insertar_wp_recarga()

		self.gestion.insertar_drones(current_mision.get_id_mision())

		parameters =[max_acce, int(max_speed)*100]
		altura= int(self.max_height_text.text())
		c = 100
		for commu in self.protocolo.commu_modules:
			commu.setFlightParameters(parameters, altura*100 + c)
			c = c+100

		self.gestion.completar_telemetrias(telemetriaV)

		distancia_wp_retorno = self.config.calcular_autonomia(float(peso),float(potenciaKg),float(Voltaje_b),float(capacidad_b),float(seguridad),float(factor_seguridad),float(dronV[0].get_velocidad_max()))

		self.trayect = Trayectorias(coords,float(max_height), float(cvh),float(cvv),float(overlap),wp_recarga)
		matriz_general = self.trayect.generar_matriz(self.n_drones,distancia_wp_retorno)

		self.dist_label.setText(str(round(self.trayect.distancia_trayectoria*1000,2)))
		self.area_label.setText(str(round(area,2)))
		counter = 0
		self.num_pws = []
		wpTotales = 0
		for dron in matriz_general:
			cont_wp = 0
			for tramo in dron:
				for wp in tramo:
					cont_wp = cont_wp+1
					if wp != tramo[-1]:
						handler.broadcast("#"+str(counter)+str(wp))
				handler.broadcast("?"+str(tramo[-2]))
			cont_wp = cont_wp+2*len(dron)
			handler.broadcast("&")
			self.num_pws.append(cont_wp)
			counter=counter+1
			wpTotales = wpTotales+cont_wp
		self.progressBar_4.setMaximum(wpTotales)

		self.gestion.insertar_wp_drones(max_height,matriz_general)
		
	def update_progress_bar(self):
		self.value = self.value+1
		with lock_progress_bar:
			self.progressBar_4.setValue(self.value)

	def db_fotos(self):
		self.config.insertar_fotos(self.fotos)
		self.report_after_finish()


	def init_trayct(self):
		self.value = 0
		self.mission_page()
		self.flag_telemetria = 1
		if self.finish_mission is None:
			self.finish_mission = MisionEndWindow(self,self.fotos)
		altura = self.max_height_text.text()	
		self.gestion.coberturas(self,self.trayect.wp_retorno_aut,self.progressBar_4,altura,self.finish_mission,self.protocolo.ns_unicos)
		self.iniciar_hilo3()
		
		self.create_grid(self.n_drones+1,4)
		self.startThread()

	def create_grid(self, rows,columns):
		self.grid = QGridLayout(self)
		header = ["Hardware id","Latitud","Longitud","Altitud"]
		self.labels = []
		for i in range(rows):
			row = []
			for j in range(columns):
				label = QLabel(header[j])
				self.grid.addWidget(label, i, j)
				row.append(label)
			self.labels.append(row)
		self.scrollAreaWidgetContents_3.setLayout(self.grid)
		
	def startThread(self):
		self.thread = Htelemetria.Worker(self.protocolo.commu_modules,self.gestion)
		self.thread.dataLoaded.connect(self.setData)
		self.thread.start()
  
	def setData(self, Posicion):
		handler.broadcast(str(Posicion[0]))
		for i in range(len(dronV)):
			pos = self.protocolo.commu_modules[i].Posicion
			pos[2] = self.gestion.coberturas[i].current_altitude
			self.labels[i+1][0].setText(dronV[i].get_hardware_id())
			for item in range(3):
				self.labels[i+1][item+1].setText(str(pos[item]))
	
	def stop_all(self):
		self.contador=self.contador+1
		if self.n_drones == self.contador:
			self.thread.stop()
			self.finish_mission.exec_()

			
		
 
	def iniciar_hilo3(self):
		self.thread2 = hilo_componente_mision.Worker(self.protocolo.commu_modules)
		self.thread2.create_frame2_signal.connect(self.create_frame2)
		self.thread2.start()

	def create_frame2(self, name_space, state):
		frame1 = CustomFrame(colors[self.n_cober], name_space, state, self.num_pws[int(name_space[-1])-1], self.gestion.coberturas[self.n_cober])
		self.layout.addWidget(frame1)
		self.gestion.coberturas[self.n_cober].frame_a_modificar(frame1)
		self.n_cober=self.n_cober+1

	def disconnect_socket(self):
		handler.on_disconnected()

	def iniciar_hilo2(self,commu):
		self.commu_objeto.append(commu)
		self.thread3 = hilo_componente_estados.Worker(commu.ns)
        # Conectamos la senal del worker a un metodo en la ventana principal
		self.thread3.create_frame_signal.connect(self.create_frame)
		self.thread3.start()

	def create_frame(self, name_space, state):
        # Este metodo sera llamado cuando el worker emita la senal
		frame = CustomFrames(name_space, state)
		self.layouts.addWidget(frame)
		self.commu_objeto[self.c].frame_a_modificar(frame)
		self.c=self.c+1


	def home_page(self):
		self.set_default_icons()
		icon = QIcon('./icons/IconoHomeGris.svg')
		self.homeBtn.setIcon(icon)
		self.homeBtn.setStyleSheet("background-color: rgb(3, 33, 77)")
		self.switchPagesStacked.setCurrentWidget(self.homePage_3)

	def mission_page(self):
		self.set_default_icons()
		icon = QIcon('./icons/IconoMisionGris.svg')
		self.missionBtn.setIcon(icon)
		self.missionBtn.setStyleSheet("background-color: rgb(3, 33, 77)")
		self.switchPagesStacked.setCurrentWidget(self.ConfiPage)
		self.stackedWidget_4.setCurrentWidget(self.page_2)
		self.stackedWidget_5.setCurrentWidget(self.page_3)

	def stop_mision(self):
		pass
		
	def console(self,text):
		with lock_console:
			self.buffer.append(text)
			

	def flush_buffer(self):
		if self.buffer:
			self.Qconsole.append('\n'.join(self.buffer))
			self.buffer = []
	    
	def report_page(self):
		self.set_default_icons()
		icon = QIcon('./icons/IconoReporteGris.svg')
		self.reportBtn.setIcon(icon)
		self.reportBtn.setStyleSheet("background-color: rgb(3, 33, 77)")
		self.switchPagesStacked.setCurrentWidget(self.reportPage)
		self.stackedWidget_2.setCurrentWidget(self.filers_widget)

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
		userSelect=self.selected_username.text().decode('utf-8')
		for user in db_user_list:
			db_user_name = user.get_nombre_usuario().decode('utf-8')
			if db_user_name == userSelect:
				self.db_user = user
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
		misions = mision_connect.get_all_missions_xUser(self.db_user.get_id_usuario())
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
		misions = mision_connect.get_all_missions_xUserANDciudad(self.db_user.get_id_usuario(), cytySelect)
		name_misions =[]
		for mision in misions:
			name_misions.append(mision.get_nombre_mision()) 
		return set(name_misions)

	def search_dates(self):
		cytySelect = self.selected_city.text()
		name_mision = self.selected_mission.text()
		dates= []
		date_conect = mision_dao_imp(conn)
		db_dates_list = date_conect.get_all_missions_xUserANDciudadANDname(self.db_user.get_id_usuario(),cytySelect,name_mision)
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
		self.label_36.setText(self.db_user.get_nombre())
		self.label_37.setText(self.db_user.get_correo())
		self.label_38.setText(self.db_user.get_celular())

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

	def report_after_finish(self):
		self.set_default_icons()
		icon = QIcon('./icons/IconoReporteGris.svg')
		self.reportBtn.setIcon(icon)
		self.reportBtn.setStyleSheet("background-color: rgb(3, 33, 77)")
		self.switchPagesStacked.setCurrentWidget(self.reportPage)
		self.stackedWidget_2.setCurrentWidget(self.report_view_widget)
		print(current_usuario.get_id_usuario(), current_usuario.get_nombre())
		print(current_mision.get_id_mision())
		print(current_wp_recarga.get_id_wp_recarga())

def on_message_received(message):
    coords_dict = json.loads(message)

    global coords
    global wp_recarga
    global area
    coords = coords_dict['wp_region'][0]
    coords.pop()
    area = coords_dict['area']
    wp_recarga = coords_dict['wp_recarga']

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    handler = server.WebSocketHandler()
    handler.message_received.connect(on_message_received)
    handler.server.listen(QtNetwork.QHostAddress.LocalHost, 8765)
    sys.exit(app.exec_())

