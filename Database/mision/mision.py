#!/usr/bin/env python

class mision:
    def __init__(self,id_mision, id_usuario, ciudad, descripcion, dimension, direccion, fecha, hora_inicio, hora_fin, nombre_mision, nombre_ubicacion, sobrelapamiento):
        self.id_mision = id_mision
        self.id_usuario = id_usuario
        self.ciudad = ciudad
        self.descripcion = descripcion
        self.dimension = dimension
        self.direccion = direccion
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.nombre_mision = nombre_mision
        self.nombre_ubicacion = nombre_ubicacion
        self.sobrelapamiento = sobrelapamiento

    def get_id_mision(self):
        return self.id_mision

    def set_id_mision(self,id_mision):
        self.id_mision = id_mision

    def get_id_usuario(self):
        return self.id_usuario

    def set_id_usuario(self,id_usuario):
        self.id_usuario = id_usuario

    def get_ciudad(self):
        return self.ciudad

    def set_ciudad(self,ciudad):
        self.ciudad = ciudad

    def get_descripcion(self):
        return self.descripcion

    def set_descripcion(self,descripcion):
        self.descripcion = descripcion

    def get_dimension(self):
        return self.dimension

    def set_dimension(self,dimension):
        self.dimension = dimension

    def get_direccion(self):
        return self.direccion

    def set_direccion(self,direccion):
        self.direccion = direccion

    def get_fecha(self):
        return self.fecha

    def set_fecha(self,fecha):
        self.fecha = fecha

    def get_hora_inicio(self):
        return self.hora_inicio

    def set_hora_inicio(self,hora_inicio):
        self.hora_inicio = hora_inicio

    def get_hora_fin(self):
        return self.hora_fin

    def set_hora_fin(self,hora_fin):
        self.hora_fin = hora_fin

    def get_nombre_mision(self):
        return self.nombre_mision

    def set_nombre_mision(self,nombre_mision):
        self.nombre_mision = nombre_mision

    def get_sobrelapamiento(self):
        return self.sobrelapamiento

    def set_sobrelapamiento(self,sobrelapamiento):
        self.sobrelapamiento = sobrelapamiento

    def get_nombre_ubicacion(self):
        return self.nombre_ubicacion

    def set_nombre_ubicacion(self,nombre_ubicacion):
        self.nombre_ubicacion = nombre_ubicacion