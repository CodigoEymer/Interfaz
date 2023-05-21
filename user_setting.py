# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_settings.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
import main

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(165, 97)
        Form.setStyleSheet("background-color: rgb(3, 33, 77);\n"
"\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setStyleSheet("QPushButton{\n"
"    padding: 3px 3px;\n"
"    border-radius: 10px;\n"
"}\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.my_dataBtn = QtWidgets.QPushButton(self.frame)
        self.my_dataBtn.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(111, 110, 110);")
        self.my_dataBtn.setObjectName("my_dataBtn")
        self.verticalLayout.addWidget(self.my_dataBtn)
        self.logoutBtn = QtWidgets.QPushButton(self.frame)
        self.logoutBtn.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(255, 0, 0);")
        self.logoutBtn.setObjectName("logoutBtn")
        self.verticalLayout.addWidget(self.logoutBtn)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.logoutBtn.clicked.connect(self.logout)
        self.my_dataBtn.clicked.connect(self.data)
        
    def logout(self):
        pass

    def data(self):
        main.signin_window()
        self.stackedWidget_3.setCurrentWidget(self.userConfiPage)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.my_dataBtn.setText(_translate("Form", "Mis datos"))
        self.logoutBtn.setText(_translate("Form", "Cerrar sesión"))


