#!/usr/bin/env python

class wp_recarga:
    def __init__(self,id_wp_recarga, id_mision, latitud_recarga, longitud_recarga, altitud_recarga):        
        self.id_wp_recarga = id_wp_recarga
        self.id_mision = id_mision
        self.latitud_recarga = latitud_recarga
        self.longitud_recarga = longitud_recarga
        self.altitud_recarga = altitud_recarga

    def get_id_wp_recarga(self):
        return self.id_wp_recarga

    def set_id_wp_recarga(self,id_wp_recarga):
        self.id_wp_recarga = id_wp_recarga

    def get_id_mision(self):
        return self.id_mision

    def set_id_mision(self,id_mision):
        self.id_mision = id_mision

    def get_latitud_recarga(self):
        return self.latitud_recarga

    def set_latitud_recarga(self,latitud_recarga):
        self.latitud_recarga = latitud_recarga

    def get_longitud_recarga(self):
        return self.longitud_recarga

    def set_longitud_recarga(self,longitud_recarga):
        self.longitud_recarga = longitud_recarga

    def get_altitud_recarga(self):
        return self.altitud_recarga

    def set_altitud_recarga(self,altitud_recarga):
        self.altitud_recarga = altitud_recarga
