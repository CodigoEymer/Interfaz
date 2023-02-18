#!/usr/bin/env python

class wp_region:
    def __init__(self,id_wp_region, id_mision, wp):        
        self.id_wp_region = id_wp_region
        self.id_mision = id_mision
        self.wp = wp

    def get_id_wp_region(self):
        return self.id_wp_region

    def set_id_wp_region(self,id_wp_region):
        self.id_wp_region = id_wp_region

    def get_id_mision(self):
        return self.id_mision

    def set_id_mision(self,id_mision):
        self.id_mision = id_mision

    def get_wp(self):
        return self.wp

    def set_wp(self,wp):
        self.wp = wp
