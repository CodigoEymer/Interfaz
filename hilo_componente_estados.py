from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal


class Worker(QThread):
    create_frame_signal = pyqtSignal(str, str)
    def __init__(self, commu):
        super(Worker, self).__init__()
        self.commu = commu

    def run(self):
        self.create_frame_signal.emit("Nada", "-*-*-*")