#!/usr/bin/env python

class wp_recarga:
    def __init__(self,id_wp_recarga = None, id_mision = None, wp = None):        
        self.id_wp_recarga = id_wp_recarga
        self.id_mision = id_mision
        self.wp = wp

    def get_id_wp_recarga(self):
        return self.id_wp_recarga

    def set_id_wp_recarga(self,id_wp_recarga):
        self.id_wp_recarga = id_wp_recarga

    def get_id_mision(self):
        return self.id_mision

    def set_id_mision(self,id_mision):
        self.id_mision = id_mision

    def get_wp(self):
        return self.wp

    def set_wp(self,wp):
        self.wp = wp
