from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
import time

class Worker(QThread):
    create_frame_signal = pyqtSignal(str, str)

    def __init__(self, ns):
        super(Worker, self).__init__()
        self.ns = ns
        print("ns",ns)
        print(type(ns))

    def run(self):
        self.create_frame_signal.emit(self.ns, "not_connected")