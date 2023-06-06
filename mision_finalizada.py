from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi
import os

class MisionEndWindow(QDialog):
    def __init__(self, parent, fotos):
        super(MisionEndWindow, self).__init__(parent)
        loadUi('mision_finalizada.ui', self)
        self.setModal(True)
        self.fotos = fotos
        self.omitBtn.clicked.connect(self.close_w)
        self.uploadPhotosBtn.clicked.connect(self.upload_photos)

    def close_w(self):
        self.close()

    def upload_photos(self):
        self.close()
        dname = QFileDialog.getExistingDirectory(self, 'Open directory', './')
        jpg_files = [os.path.join(dname, filename) for filename in os.listdir(dname) if filename.endswith('.jpg')]

        foto_dict = {(foto.get_id_dron(), foto.get_hora_captura()): foto for foto in self.fotos}

        for file_path in jpg_files:
            filename = os.path.basename(file_path)
            sin_extension = os.path.splitext(filename)[0]
            id_y_hora = sin_extension.split('_')

            id, hora = id_y_hora

            foto = foto_dict.get((id, hora))

            if foto:
                with open(file_path, "rb") as file:
                    data = file.read()
                    foto.set_foto(data)
                                
                    
