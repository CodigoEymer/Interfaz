from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar
import time
import communication_module

class Worker(QThread):
    dataLoaded = pyqtSignal(list)
    def __init__(self, commu_module):
        super(Worker, self).__init__()
        self.commu_module = commu_module

    def run(self):
        while(True):
            lista = []
            for comm in self.commu_module:
                data = comm.Posicion
                lista.append(data)
            self.dataLoaded.emit(lista)
            time.sleep(3)    