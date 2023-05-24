from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi

class SecondWindow(QWidget):
    def __init__(self):
        super(SecondWindow, self).__init__()
        loadUi('user_settings.ui', self)
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        x = rect.width() - self.width()
        y = 100
        self.move(int(x), int(y))
        self.logoutBtn.clicked.connect(self.logout)
        self.my_dataBtn.clicked.connect(self.data)

    def logout(self):
        print("it works!!")

    def data(self):
        print("it works")