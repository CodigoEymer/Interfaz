from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class SecondWindow(QDialog):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        loadUi('user_settings.ui', self)
        self.setModal(True)
        
        self.logoutBtn.clicked.connect(parent.logout)
        self.my_dataBtn.clicked.connect(parent.update_user_data)
        
