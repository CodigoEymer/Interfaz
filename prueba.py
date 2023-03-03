from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar
import time

class Worker(QThread):
    progress = pyqtSignal(int)

    def run(self):
        print("Hello world")
        for i in range(101):
            self.progress.emit(i)
            time.sleep(0.2)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Thread Example')
        self.setGeometry(100, 100, 400, 200)

        self.button = QPushButton('Start', self)
        self.button.move(20, 20)
        self.button.clicked.connect(self.startThread)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(20, 50, 360, 30)

    def startThread(self):
        self.thread = Worker()
        self.thread.progress.connect(self.setProgress)
        self.thread.start()

    def setProgress(self, value):
        self.progressBar.setValue(value)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
