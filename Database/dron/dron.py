#!/usr/bin/env python

class dron:
    def __init__(self, id_dron,id_mision, aceleracion_max, velocidad_max,altura_max,campo_vision,controladora,duracion_bateria,tipo):
        self.id_dron = id_dron
        self.id_mision = id_mision
        self.aceleracion_max = aceleracion_max
        self.velocidad_max =velocidad_max
        self.altura_max =altura_max
        self.campo_vision =campo_vision
        self.controladora =controladora
        self.duracion_bateria =duracion_bateria
        self.tipo =tipo

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

    def get_altura_max(self):
        return self.altura_max

    def set_altura_max(self, altura_max):
        self.altura_max =  altura_max

    def get_campo_vision(self):
        return self.campo_vision

    def set_campo_vision(self, campo_vision):
        self.campo_vision =  campo_vision

    def get_controladora(self):
        return self.controladora

    def set_controladora(self, controladora):
        self.controladora =  controladora

    def get_duracion_bateria(self):
        return self.duracion_bateria

    def set_duracion_bateria(self, duracion_bateria):
        self.duracion_bateria =  duracion_bateria

    def get_tipo(self):
        return self.tipo

    def set_tipo(self, tipo):
        self.tipo =  tipo