#!/usr/bin/env python
import MySQLdb
import wp_region
import wp_region_dao

        
class wp_region_dao_imp:
    def __init__(self, conn):
        self.wp_region_list = []
        self.tupla = ()
        self.connection = conn
        cursor = self.connection.cursor()
        query="select id_wp_region, id_mision, latitud_region, longitud_region, altitud_region from wp_region"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            wp_region_obj = wp_region.wp_region(tupla[i][0],tupla[i][1],tupla[i][2],tupla[i][3], tupla[i][4])
            self.wp_region_list.append(wp_region_obj)
        cursor.close()

    def insert_wp_region(self, id_mision, latitud_region, longitud_region, altitud_region):
        res_rows = 0
        query="INSERT INTO wp_region SET id_mision='"+id_mision+"',latitud_region='"+latitud_region+"', longitud_region='"+longitud_region+"', altitud_region='"+altitud_region+"'"
        cursor = self.connection.cursor()
        res_rows = cursor.execute(query)
        self.connection.commit()
        
        cursor.close()
        return res_rows