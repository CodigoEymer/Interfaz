#!/usr/bin/env python

class foto:
    def __init__(self, id_dron, foto, hora_captura,latitud_captura,longitud_captura,altitud_captura):
        #self.id_foto
        self.id_dron = id_dron
        self.foto =foto
        self.hora_captura =hora_captura
        self.latitud_captura =latitud_captura
        self.longitud_captura =longitud_captura
        self.altitud_captura =altitud_captura

    def get_id_dron(self):
        return self.id_dron

    def set_id_dron(self,id_dron):
        self.id_dron = id_dron

    def get_id_foto(self):
        return self.id_foto

    def set_id_foto(self, id_foto):
        self.id_foto = id_foto

    def get_foto(self):
        return self.foto

    def set_foto(self, foto):
        self.foto = foto

    def get_hora_captura(self):
        return self.hora_captura

    def set_hora_captura(self, hora_captura):
        self.hora_captura = hora_captura

    def get_latitud_captura(self):
        return self.latitud_captura

    def set_latitud_captura(self, latitud_captura):
        self.latitud_captura =  latitud_captura

    def get_longitud_captura(self):
        return self.longitud_captura

    def set_longitud_captura(self, longitud_captura):
        self.longitud_captura =  longitud_captura

    def get_altitud_captura(self):
        return self.altitud_captura

    def set_altitud_captura(self, altitud_captura):
        self.altitud_captura =  altitud_captura