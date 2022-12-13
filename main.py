import sys
import os
import rospy
import rospkg
import resources_rc

from std_msgs.msg import String
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

from mavros_msgs.srv import *


class MainWindow(QMainWindow):

    def __init__(self):
	super(MainWindow, self).__init__()
	loadUi('interface.ui', self)
	
	self.ingresarBtn.clicked.connect(self.settings_page)
	self.crearUsuarioBtn.clicked.connect(self.signup_page)
	self.registerBtn.clicked.connect(self.login_page)
	self.cancelRegisterBtn.clicked.connect(self.login_page)	
	self.settingsBtn.clicked.connect(self.settings_page)
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
            #http://wiki.ros.org/mavros/CustomModes for custom modes
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

