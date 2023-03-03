from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar
import time
import communication_module

class Worker(QThread):
    dataLoaded = pyqtSignal(list)
    
    def run(self):
        data = communication_module.communication_module.Dron
        self.dron.emit(data)


