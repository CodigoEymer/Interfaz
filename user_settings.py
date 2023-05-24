from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class SecondWindow(QDialog):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        loadUi('user_settings.ui', self)
        self.setModal(True)
        
        self.logoutBtn.clicked.connect(self.logout)
        self.my_dataBtn.clicked.connect(self.data)
        

    def logout(self):
        print("it works!!")

    def data(self):
        print("it works")