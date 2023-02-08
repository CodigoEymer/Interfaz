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
import server

from folium.plugins import Draw
import geocoder
from std_msgs.msg import String
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebSockets
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
		
		self.ingresarBtn.clicked.connect(self.user_validation)
		self.crearUsuarioBtn.clicked.connect(self.signup_page)
		self.registerBtn.clicked.connect(self.register_button)
		self.cancelRegisterBtn.clicked.connect(self.login_page)	
		self.settingsBtn.clicked.connect(self.home_page)
		self.generarTrayectBtn.clicked.connect(self.gen_tray)
		#self.pushButton_20.clicked.connect(self.get_location)
		self.homeBtn.clicked.connect(self.settings_page)
		self.connectionBtn.clicked.connect(self.connection_page)
		self.telemetryBtn.clicked.connect(self.telemetry_page_2)
		self.missionBtn.clicked.connect(self.mission_page)
		self.playBtn.clicked.connect(self.armar)
		self.pauseBtn.clicked.connect(self.pausingMission)
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
		self.main_window()
		self.switchPagesStacked.setCurrentWidget(self.ConfiPage)
		m.add_child(draw)
		data = io.BytesIO()
		m.save(data, close_file = False)
		#self.webView.setHtml(data.getvalue().decode())
		html = r"""
		
<!DOCTYPE html>
<html><head>
    <title>Leaflet.draw vector editing handlers</title>

    <script src="libs/leaflet-src.js"></script>
    <link rel="stylesheet" href="libs/leaflet.css">

    <script src="../../src/Leaflet.draw.js"></script>
    <script src="../../src/Leaflet.Draw.Event.js"></script>
    <link rel="stylesheet" href="../../src/leaflet.draw.css">

    <script src="../../src/Toolbar.js"></script>
    <script src="../../src/Tooltip.js"></script>

    <script src="../../src/ext/GeometryUtil.js"></script>
    <script src="../../src/ext/LatLngUtil.js"></script>
    <script src="../../src/ext/LineUtil.Intersect.js"></script>
    <script src="../../src/ext/Polygon.Intersect.js"></script>
    <script src="../../src/ext/Polyline.Intersect.js"></script>
    <script src="../../src/ext/TouchEvents.js"></script>

    <script src="../../src/draw/DrawToolbar.js"></script>
    <script src="../../src/draw/handler/Draw.Feature.js"></script>
    <script src="../../src/draw/handler/Draw.SimpleShape.js"></script>
    <script src="../../src/draw/handler/Draw.Polyline.js"></script>
    <script src="../../src/draw/handler/Draw.Marker.js"></script>
    <script src="../../src/draw/handler/Draw.Circle.js"></script>
    <script src="../../src/draw/handler/Draw.CircleMarker.js"></script>
    <script src="../../src/draw/handler/Draw.Polygon.js"></script>
    <script src="../../src/draw/handler/Draw.Rectangle.js"></script>


    <script src="../../src/edit/EditToolbar.js"></script>
    <script src="../../src/edit/handler/EditToolbar.Edit.js"></script>
    <script src="../../src/edit/handler/EditToolbar.Delete.js"></script>

    <script src="../../src/Control.Draw.js"></script>

    <script src="../../src/edit/handler/Edit.Poly.js"></script>
    <script src="../../src/edit/handler/Edit.SimpleShape.js"></script>
    <script src="../../src/edit/handler/Edit.Rectangle.js"></script>
    <script src="../../src/edit/handler/Edit.Marker.js"></script>
    <script src="../../src/edit/handler/Edit.CircleMarker.js"></script>
    <script src="../../src/edit/handler/Edit.Circle.js"></script>
</head>
<body>
<div id="map" style="width: 800px; height: 600px; border: 1px solid rgb(204, 204, 204); position: relative;" class="leaflet-container leaflet-touch leaflet-fade-anim leaflet-grab leaflet-touch-drag leaflet-touch-zoom" tabindex="0"><div class="leaflet-pane leaflet-map-pane" style="transform: translate3d(0px, 0px, 0px);"><div class="leaflet-pane leaflet-tile-pane"><div class="leaflet-layer " style="z-index: 1; opacity: 1;"><div class="leaflet-tile-container leaflet-zoom-animated" style="z-index: 18; transform: translate3d(0px, 0px, 0px) scale(1);"><img alt="" role="presentation" src="http://b.tile.openstreetmap.org/13/4094/2723.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(121px, 9px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://c.tile.openstreetmap.org/13/4095/2723.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(377px, 9px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://c.tile.openstreetmap.org/13/4094/2724.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(121px, 265px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://a.tile.openstreetmap.org/13/4095/2724.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(377px, 265px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://a.tile.openstreetmap.org/13/4094/2722.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(121px, -247px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://b.tile.openstreetmap.org/13/4095/2722.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(377px, -247px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://a.tile.openstreetmap.org/13/4093/2723.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(-135px, 9px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://a.tile.openstreetmap.org/13/4096/2723.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(633px, 9px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://b.tile.openstreetmap.org/13/4093/2724.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(-135px, 265px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://b.tile.openstreetmap.org/13/4096/2724.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(633px, 265px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://a.tile.openstreetmap.org/13/4094/2725.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(121px, 521px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://b.tile.openstreetmap.org/13/4095/2725.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(377px, 521px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://c.tile.openstreetmap.org/13/4093/2722.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(-135px, -247px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://c.tile.openstreetmap.org/13/4096/2722.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(633px, -247px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://c.tile.openstreetmap.org/13/4093/2725.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(-135px, 521px, 0px); opacity: 1;"><img alt="" role="presentation" src="http://c.tile.openstreetmap.org/13/4096/2725.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(633px, 521px, 0px); opacity: 1;"></div></div></div><div class="leaflet-pane leaflet-shadow-pane"></div><div class="leaflet-pane leaflet-overlay-pane"></div><div class="leaflet-pane leaflet-marker-pane"></div><div class="leaflet-pane leaflet-tooltip-pane"></div><div class="leaflet-pane leaflet-popup-pane"></div><div class="leaflet-proxy leaflet-zoom-animated"></div></div><div class="leaflet-control-container"><div class="leaflet-top leaflet-left"><div class="leaflet-control-zoom leaflet-bar leaflet-control"></div><div class="leaflet-control-layers leaflet-control-layers-expanded leaflet-control" aria-haspopup="true"><form class="leaflet-control-layers-list"><div class="leaflet-control-layers-base"><label><div><input type="radio" class="leaflet-control-layers-selector" name="leaflet-base-layers" checked="checked"><span> osm</span></div></label><label><div><input type="radio" class="leaflet-control-layers-selector" name="leaflet-base-layers"><span> google</span></div></label></div><div class="leaflet-control-layers-separator"></div><div class="leaflet-control-layers-overlays"><label><div><input type="checkbox" class="leaflet-control-layers-selector" checked=""><span> drawlayer</span></div></label></div></form></div><div class="leaflet-draw leaflet-control"><div class="leaflet-draw-section"><div class="leaflet-draw-toolbar leaflet-bar leaflet-draw-toolbar-top"></div><ul class="leaflet-draw-actions"></ul></div><div class="leaflet-draw-section"><div class="leaflet-draw-toolbar leaflet-bar"></div><ul class="leaflet-draw-actions"></ul></div></div></div><div class="leaflet-top leaflet-right"></div><div class="leaflet-bottom leaflet-left"></div><div class="leaflet-bottom leaflet-right"><div class="leaflet-control-attribution leaflet-control"><a href="http://leafletjs.com" title="A JS library for interactive maps">Leaflet</a> |  <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors</div></div></div></div>

<script>
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            osm = L.tileLayer(osmUrl, { maxZoom: 18, attribution: osmAttrib }),
            map = new L.Map('map', { center: new L.LatLng(51.505, -0.04), zoom: 13 }),
            drawnItems = L.featureGroup().addTo(map);
    L.control.layers({
        'osm': osm.addTo(map),
        "google": L.tileLayer('http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}', {
            attribution: 'google'
        })
    }, { 'drawlayer': drawnItems }, { position: 'topleft', collapsed: false }).addTo(map);
    map.addControl(new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            poly: {
                allowIntersection: false
            }
        },
        draw: {
            polygon: {
                allowIntersection: false,
                showArea: true
            }
        }
    }));

    map.on(L.Draw.Event.CREATED, function (event) {
        var layer = event.layer;

        drawnItems.addLayer(layer);
    });

</script>


</body></html>
		
		"""
		self.webView.setHtml(html)

	def user_validation(self):
		
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

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    serverObject = QtWebSockets.QWebSocketServer('My Socket', QtWebSockets.QWebSocketServer.NonSecureMode)
    server = server.MyServer(serverObject)
    serverObject.closed.connect(app.quit)
    sys.exit(app.exec_())
