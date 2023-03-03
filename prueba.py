from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar
import time
import communication_module

class Worker(QThread):
    dataLoaded = pyqtSignal(list)
    
    def run(self):
        while(True):
            data = communication_module.communication_module.Posiciones
            self.dataLoaded.emit(data)
            time.sleep(0.05)

