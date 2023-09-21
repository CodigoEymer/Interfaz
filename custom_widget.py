from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class CustomFrame(QFrame):
    def __init__(self, dron_id, estado, num_wp_total, parent=None):
        super(CustomFrame, self).__init__(parent)
        self.setStyleSheet("background-color: #FFFFFF;")
        
        self.layout = QHBoxLayout(self)

        self.button1 = QPushButton(dron_id)
        self.button1.setStyleSheet("QPushButton {background-color: #E65E5C; color: white;}")

        self.button2 = QPushButton(estado)
        self.button2.setStyleSheet("QPushButton {background-color: #FF9800; color: white;}")

        self.button3 = QPushButton("100%")
        self.button3.setIcon(QIcon('./icons/batteryVerde.svg'))
        self.button3.setIconSize(QSize(24, 24))

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("background-color: #729fcf;")
        self.progress_bar.setAlignment(Qt.AlignCenter)
        
        self.progress_bar.setMaximum(num_wp_total)
        self.progress_bar.setValue(19)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.progress_bar)
