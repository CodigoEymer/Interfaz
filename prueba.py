from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar
import time
import communication_module

class Worker(QThread):
    dataLoaded = pyqtSignal(list)
    def __init__(self, commu_module, gestion):
        super(Worker, self).__init__()
        self.commu_module = commu_module
        self.gestion = gestion

    def run(self):
        while(True):
            lista = []
            colores = self.gestion.definir_color()
            for i in range(self.commu_module):
                latitud = self.commu_module[i].Posicion[0]
                longitud = self.commu_module[i].Posicion[1]
                wp = (latitud,longitud)
                lista.append([colores[i],wp])
                lista.append([colores[i],wp])
            self.dataLoaded.emit(lista)
            time.sleep(1)