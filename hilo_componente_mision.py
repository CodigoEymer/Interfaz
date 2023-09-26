from PyQt5.QtCore import QThread, pyqtSignal


class Worker(QThread):
    create_frame2_signal = pyqtSignal(str, str)

    def __init__(self, commus):
        super(Worker, self).__init__()
        self.commus = commus

    def run(self):
        for commu in self.commus:
            self.create_frame2_signal.emit(commu.ns, "Mssion")