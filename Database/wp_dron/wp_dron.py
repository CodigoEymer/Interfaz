#!/usr/bin/env python

class wp_dron:
    def __init__(self,id_wp_dron, id_dron, latitud_ruta, longitud_ruta, altitud_ruta):        
        self.id_wp_dron = id_wp_dron
        self.id_dron = id_dron
        self.latitud_ruta = latitud_ruta
        self.longitud_ruta = longitud_ruta
        self.altitud_ruta = altitud_ruta

    def get_id_wp_dron(self):
        return self.id_wp_dron

    def set_id_wp_dron(self,id_wp_dron):
        self.id_wp_dron = id_wp_dron

    def get_id_dron(self):
        return self.id_dron

    def set_id_dron(self,id_dron):
        self.id_dron = id_dron

    def get_latitud_ruta(self):
        return self.latitud_ruta

    def set_latitud_ruta(self,latitud_ruta):
        self.latitud_ruta = latitud_ruta

    def get_longitud_ruta(self):
        return self.longitud_ruta

    def set_longitud_ruta(self,longitud_ruta):
        self.longitud_ruta = longitud_ruta

    def get_altitud_ruta(self):
        return self.altitud_ruta

    def set_altitud_ruta(self,altitud_ruta):
        self.altitud_ruta = altitud_ruta
