#!/usr/bin/env python

class telemetria:
    def __init__(self, id_dron, porcentaje_bateria, hora_actualizacion,latitud,longitud,altitud,cabeceo,guinada,alabeo,salud_camara,salud_gps,salud_controladora):
        #self.id_telemetria
        self.id_dron = id_dron
        self.porcentaje_bateria =porcentaje_bateria
        self.hora_actualizacion =hora_actualizacion
        self.latitud =latitud
        self.longitud =longitud
        self.altitud =altitud
        self.cabeceo =cabeceo
        self.guinada =guinada
        self.alabeo =alabeo
        self.salud_camara =salud_camara
        self.salud_gps =salud_gps
        self.salud_controladora =salud_controladora

    def get_id_telemetria(self):
        return self.id_telemetria

    def set_id_telemetria(self,id_telemetria):
        self.id_telemetria = id_telemetria

    def get_id_dron(self):
        return self.id_dron

    def set_id_dron(self,id_dron):
        self.id_dron = id_dron

    def get_porcentaje_bateria(self):
        return self.porcentaje_bateria

    def set_porcentaje_bateria(self, porcentaje_bateria):
        self.porcentaje_bateria = porcentaje_bateria

    def get_hora_actualizacion(self):
        return self.hora_actualizacion

    def set_hora_actualizacion(self, hora_actualizacion):
        self.hora_actualizacion = hora_actualizacion

    def get_latitud(self):
        return self.latitud

    def set_latitud(self, latitud):
        self.latitud =  latitud

    def get_longitud(self):
        return self.longitud

    def set_longitud(self, longitud):
        self.longitud =  longitud

    def get_altitud(self):
        return self.altitud

    def set_altitud(self, altitud):
        self.altitud =  altitud

    def get_cabeceo(self):
        return self.cabeceo

    def set_cabeceo(self, cabeceo):
        self.cabeceo =  cabeceo

    def get_guinada(self):
        return self.guinada

    def set_guinada(self, guinada):
        self.guinada =  guinada

    def get_alabeo(self):
        return self.alabeo

    def set_alabeo(self, alabeo):
        self.alabeo =  alabeo

    def get_salud_camara(self):
        return self.salud_camara

    def set_salud_camara(self, salud_camara):
        self.salud_camara =  salud_camara
        
    def get_salud_gps(self):
        return self.salud_gps

    def set_salud_gps(self, salud_gps):
        self.salud_gps =  salud_gps  

    def get_salud_controladora(self):
        return self.salud_controladora

    def set_salud_controladora(self, salud_controladora):
        self.salud_controladora =  salud_controladora  