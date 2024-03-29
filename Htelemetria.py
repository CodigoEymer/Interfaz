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
        self.running = True
        
    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            lista = []
            listastr =[]
            colores = self.gestion.definir_color()
            for i in range(len(self.commu_module)):
                latitud = self.commu_module[i].Posicion[0]
                longitud = self.commu_module[i].Posicion[1]
                wp = (latitud,longitud)
                lista.append([colores[i],wp])
                lista.append([colores[i],wp])
            dato =str(lista)
            listastr.append(dato)
            
            self.dataLoaded.emit(listastr)
            time.sleep(2) 