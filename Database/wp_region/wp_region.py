#!/usr/bin/env python

class wp_region:
    def __init__(self,id_wp_region, id_mision, latitud_region, longitud_region, altitud_region):        
        self.id_wp_region = id_wp_region
        self.id_mision = id_mision
        self.latitud_region = latitud_region
        self.longitud_region = longitud_region
        self.altitud_region = altitud_region

    def get_id_wp_region(self):
        return self.id_wp_region

    def set_id_wp_region(self,id_wp_region):
        self.id_wp_region = id_wp_region

    def get_id_mision(self):
        return self.id_mision

    def set_id_mision(self,id_mision):
        self.id_mision = id_mision

    def get_latitud_region(self):
        return self.latitud_region

    def set_latitud_region(self,latitud_region):
        self.latitud_region = latitud_region

    def get_longitud_region(self):
        return self.longitud_region

    def set_longitud_region(self,longitud_region):
        self.longitud_region = longitud_region

    def get_altitud_region(self):
        return self.altitud_region

    def set_altitud_region(self,altitud_region):
        self.altitud_region = altitud_region

