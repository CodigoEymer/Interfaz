#!/usr/bin/env python
import MySQLdb
import wp_recarga
import wp_recarga_dao

        
class wp_recarga_dao_imp:
    def __init__(self, conn):
        self.wp_recarga_list = []
        self.tupla = ()
        self.connection = conn
        cursor = self.connection.cursor()
        query="select id_wp_recarga, id_mision, latitud_recarga, longitud_recarga, altitud_recarga from wp_recarga"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            wp_recarga_obj = wp_recarga.wp_recarga(tupla[i][0],tupla[i][1],tupla[i][2],tupla[i][3], tupla[i][4])
            self.wp_recarga_list.append(wp_recarga_obj)
        cursor.close()

    def insert_wp_recarga(self, id_mision, latitud_recarga, longitud_recarga, altitud_recarga):
        res_rows = 0
        query="INSERT INTO wp_recarga SET id_mision='"+id_mision+"',latitud_recarga='"+latitud_recarga+"', longitud_recarga='"+longitud_recarga+"', altitud_recarga='"+altitud_recarga+"'"
        cursor = self.connection.cursor()
        res_rows = cursor.execute(query)
        self.connection.commit()
        
        cursor.close()
        return res_rows