#!/usr/bin/env python

class usuarios:
    def __init__(self,id_usuario, nombre, nombre_usuario, correo, celular):
        self.id_usuario = id_usuario
        self.celular = celular   
        self.nombre = nombre
        self.correo = correo
        self.nombre_usuario =nombre_usuario
        

    def get_celular(self):
        return self.celular

    def set_celular(self,celular):
        self.celular = celular

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_correo(self):
        return self.correo

    def set_correo(self, correo):
        self.correo = correo

    def get_nombre_usuario(self):
        return self.nombre_usuario

    def set_nombre_usuario(self, nombre_usuario):
        self.nombre_usuario =  nombre_usuario

    def get_id_usuario(self):
        return self.id_usuario

    def set_id_usuario(self, id_usuario):
        self.id_usuario = id_usuario
        