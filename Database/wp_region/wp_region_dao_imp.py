#!/usr/bin/env python
import MySQLdb
import wp_region
import wp_region_dao

        
class wp_region_dao_imp():

    def __init__(self, conn):
        self.wp_region_list = []
        self.tupla = ()
        self.connection = conn
        cursor = self.connection.cursor()
        query="select id_wp_region, id_mision, wp from wp_region"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            wp_region_obj = wp_region.wp_region(tupla[i][0],tupla[i][1],tupla[i][2])
            self.wp_region_list.append(wp_region_obj)
        cursor.close()

    def insert_wp_region(self, id_mision, wp):
        res_rows = 0
        query="INSERT INTO wp_region SET id_mision='"+id_mision+"',wp='"+wp+"'"
        cursor = self.connection.cursor()
        res_rows = cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return res_rows

    def get_all_wp_region(self, id_mision):
        self.wps= []
        query="select id_wp_region, wp from wp_region where id_mision=" + str(id_mision)
        cursor = self.connection.cursor()
        result = cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            wp = wp_region.wp_region(tupla[i][0],id_mision, tupla[i][1])
            self.wps.append(wp)
        cursor.close()
        return self.wps