# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi

class SecondWindow(QWidget):
    def __init__(self):

        super(SecondWindow, self).__init__()
        loadUi('user_settings.ui', self)

        self.logoutBtn.clicked.connect(self.logout)
        self.my_dataBtn.clicked.connect(self.data)

    def logout(self):
        print("it works!!")

    def data(self):
        print("it works")



if __name__ == "__main__":
    app = QApplication([])
    ex = SecondWindow()
    # get screen size
    screen = app.primaryScreen()
    rect = screen.availableGeometry()

    # calculate desired position (for example, center of the screen)
    x = rect.width() - ex.width()
    y = 100

    # move window
    ex.move(int(x), int(y))
    ex.show()
    sys.exit(app.exec_())