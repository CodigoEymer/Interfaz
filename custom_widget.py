from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class CustomFrame(QFrame):
    def __init__(self, color, ns, estado, num_wp_total, cobertura, parent=None):
        super(CustomFrame, self).__init__(parent)
        self.cobertura=cobertura
        self.setStyleSheet("background-color: #FFFFFF;")
        
        self.layout = QHBoxLayout(self)

        self.button1 = QPushButton(ns)
        self.button1.setStyleSheet("QPushButton {background-color: "+color+"; color: black;}")

        self.button2 = QPushButton(estado)
        self.button2.setStyleSheet("QPushButton {background-color: #FF9800; color: black;}")

        self.button3 = QPushButton("100%")
        self.button3.setIcon(QIcon('./icons/batteryVerde.svg'))
        self.button3.setIconSize(QSize(24, 24))

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("background-color: #729fcf;")
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setMaximum(num_wp_total)
        self.progress_bar.setValue(0)
        
        self.continue_button = QPushButton()
        self.continue_button.setIcon(QIcon('./icons/feather/play-circle.svg'))
        self.continue_button.setStyleSheet("QPushButton {background-color: #4e9a06;}")

        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.layout.addWidget(self.continue_button)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.progress_bar)
        
        self.continue_button.clicked.connect(self.reanudar_mision)
    
    def reanudar_mision(self):
        self.cobertura.reanudar_mision()
