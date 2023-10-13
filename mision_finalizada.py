from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi
import os

class MisionEndWindow(QDialog):
    def __init__(self, parent, fotos):
        super(MisionEndWindow, self).__init__(parent)
        loadUi('mision_finalizada.ui', self)
        self.setModal(True)
        self.fotos = fotos
        self.parent = parent
        self.omitBtn.clicked.connect(self.close_w)
        self.uploadPhotosBtn.clicked.connect(self.upload_photos)

    def close_w(self):
        self.close()

    def upload_photos(self):
        self.close()
        dname = QFileDialog.getExistingDirectory(self, 'Open directory', './')
        for filename in os.listdir(dname):
            if filename.endswith('.jpg'):
                with open(os.path.join(dname, filename), "rb") as file:
                    data = file.read()
                    partes = filename.split('/')
                    ultima_parte = partes[-1]
                    sin_extension = ultima_parte.split('.jpg')[0]
                    id_y_hora = sin_extension.split('_')
                    id = id_y_hora[0]
                    hora = id_y_hora[1]
                    for foto in self.fotos:
                        if foto.get_id_dron()==id and foto.get_hora_captura()==hora:
                                foto.set_foto(data)
        self.parent.db_fotos()
        
         