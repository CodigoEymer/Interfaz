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

        self.button2 = QPushButton(estado)
        self.button2.setStyleSheet("QPushButton {background-color: #FF9800; color: white;}")

        self.button3 = QPushButton()
        self.button3.setIcon(QIcon('./icons/batteryRojo.svg'))
        self.button3.setIconSize(QSize(30, 30))
        
        self.button4 = QPushButton()
        self.button4.setIcon(QIcon('./icons/gpsRojo.svg'))
        self.button4.setIconSize(QSize(30, 30))
        
        self.button5 = QPushButton()
        self.button5.setIcon(QIcon('./icons/motorRojo.svg'))
        self.button5.setIconSize(QSize(30, 30))
        
        self.button6 = QPushButton()
        self.button6.setIcon(QIcon('./icons/cpuRojo.svg'))
        self.button6.setIconSize(QSize(30, 30))
        
        self.button7 = QPushButton()
        self.button7.setIcon(QIcon('./icons/imuRojo.svg'))
        self.button7.setIconSize(QSize(30, 30))
        
        self.button8 = QPushButton()
        self.button8.setIcon(QIcon('./icons/cameraRojo.svg'))
        self.button8.setIconSize(QSize(30, 30))

        #self.spacerItem = QSpacerItem(584, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        #self.layout.addWidget(self.spacerItem)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button4)
        self.layout.addWidget(self.button5)
        self.layout.addWidget(self.button6)
        self.layout.addWidget(self.button7)
        self.layout.addWidget(self.button8)
