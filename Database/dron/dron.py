#!/usr/bin/env python

class dron:
    def __init__(self,id_dron= None, id_mision= None,ac_max= None,vel_max= None,alt_max= None,cvH= None,cvV= None,controladora= "None",voltaje_inicial= "2.5",tipo= "None",hardware_id ="2.4"):
        self.id_dron = id_dron
        self.id_mision = id_mision
        self.aceleracion_max = ac_max
        self.velocidad_max =vel_max
        self.altura_max =alt_max
        self.cvH =cvH
        self.controladora =controladora
        self.voltaje_inicial =voltaje_inicial
        self.tipo =tipo
        self.cvV = cvV
        self.hardware_id = hardware_id

    def get_id_dron(self):
        return self.id_dron

    def set_id_dron(self,id_dron):
        self.id_dron = id_dron

    def get_id_mision(self):
        return self.id_mision

    def set_id_mision(self, id_mision):
        self.id_mision = id_mision

    def get_aceleracion_max(self):
        return self.aceleracion_max

    def set_aceleracion_max(self, aceleracion_max):
        self.aceleracion_max = aceleracion_max

    def get_velocidad_max(self):
        return self.velocidad_max

    def set_velocidad_max(self, velocidad_max):
        self.velocidad_max = velocidad_max

    def get_altura_max(self):
        return self.altura_max

    def set_altura_max(self, altura_max):
        self.altura_max =  altura_max

    def get_cvH(self):
        return self.cvH

    def set_cvH(self, cvH):
        self.cvH =  cvH

    def get_cvV(self):
        return self.cvV

    def set_cvV(self, cvV):
        self.cvV =  cvV

    def get_controladora(self):
        return self.controladora

    def set_controladora(self, controladora):
        self.controladora =  controladora

    def get_voltaje_inicial(self):
        return self.voltaje_inicial

    def set_voltaje_inicial(self, voltaje_inicial):
        self.voltaje_inicial =  voltaje_inicial

    def get_tipo(self):
        return self.tipo

    def set_tipo(self, tipo):
        self.tipo =  tipo

    def get_hardware_id(self):
        return self.hardware_id

    def set_hardware_id(self, hardware_id):
        self.hardware_id =  hardware_id