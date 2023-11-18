from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar
import time
import communication_module

class Worker(QThread):
    flagU = pyqtSignal(str)
    def __init__(self, flag):
        super(Worker, self).__init__()
        self.flag =flag
        self.running = True
        
    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            self.flagU.emit("Hola")        
            time.sleep(2) 