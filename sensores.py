from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class CustomFrames(QFrame):
    def __init__(self, dron_id, estado, parent=None):
        super(CustomFrames, self).__init__(parent)
        self.setStyleSheet("background-color: #FFFFFF;")
        
        self.layout = QHBoxLayout(self)

        self.button1 = QPushButton(dron_id)
        self.button1.setStyleSheet("QPushButton {background-color: #E65E5C; color: white;}")

        self.button_estado = QPushButton(estado)
        self.button_estado.setStyleSheet("QPushButton {background-color: #FF9800; color: white;}")

        self.batteryBtn = QPushButton()
        self.batteryBtn.setIcon(QIcon('./icons/batteryRojo.svg'))
        self.batteryBtn.setIconSize(QSize(30, 30))
        
        self.gpsBtn = QPushButton()
        self.gpsBtn.setIcon(QIcon('./icons/gpsRojo.svg'))
        self.gpsBtn.setIconSize(QSize(30, 30))
        
        self.motorBtn = QPushButton()
        self.motorBtn.setIcon(QIcon('./icons/motorRojo.svg'))
        self.motorBtn.setIconSize(QSize(30, 30))
        
        self.autopilotBtn = QPushButton()
        self.autopilotBtn.setIcon(QIcon('./icons/cpuRojo.svg'))
        self.autopilotBtn.setIconSize(QSize(30, 30))
        
        self.imuBtn = QPushButton()
        self.imuBtn.setIcon(QIcon('./icons/imuRojo.svg'))
        self.imuBtn.setIconSize(QSize(30, 30))
        
        self.cameraBtn = QPushButton()
        self.cameraBtn.setIcon(QIcon('./icons/cameraRojo.svg'))
        self.cameraBtn.setIconSize(QSize(30, 30))


        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button_estado)
        self.layout.addWidget(self.batteryBtn)
        self.layout.addWidget(self.gpsBtn)
        self.layout.addWidget(self.motorBtn)
        self.layout.addWidget(self.autopilotBtn)
        self.layout.addWidget(self.imuBtn)
        self.layout.addWidget(self.cameraBtn)
