#!/usr/bin/env python
import MySQLdb
import wp_dron
import wp_dron_dao

        
class wp_dron_dao_imp:
    def __init__(self, conn):
        self.wp_dron_list = []
        self.tupla = ()
        self.connection = conn
        cursor = self.connection.cursor()
        query="select id_wp_dron, id_dron, latitud_ruta, longitud_ruta, altitud_ruta from wp_dron"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            wp_dron_obj = wp_dron.wp_dron(tupla[i][0],tupla[i][1],tupla[i][2],tupla[i][3], tupla[i][4])
            self.wp_dron_list.append(wp_dron_obj)
        cursor.close()

    def insert_wp_dron(self, id_dron, latitud_ruta, longitud_ruta, altitud_ruta):
        res_rows = 0
        query="INSERT INTO wp_dron SET id_dron='"+str(id_dron)+"',latitud_ruta='"+str(latitud_ruta)+"', longitud_ruta='"+str(longitud_ruta)+"', altitud_ruta='"+str(altitud_ruta)+"'"
        
        cursor = self.connection.cursor()
        res_rows = cursor.execute(query)
        self.connection.commit()
        
        cursor.close()
        return res_rows