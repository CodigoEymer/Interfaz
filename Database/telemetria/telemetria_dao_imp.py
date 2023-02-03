#!/usr/bin/env python
import MySQLdb
import telemetria
import dbconnection

        
class telemetria_dao_imp:
    def __init__(self, conn):
        self.telemetrias = []
        self.tupla = ()
        self.connection = conn
        cursor = self.connection.cursor()
        query="select id_telemetria, id_dron, porcentaje_bateria, hora_actualizacion,latitud,longitud,altitud,cabeceo,guinada,alabeo,salud_camara,salud_gps,salud_controladora from Telemetria"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            telemetria1 = telemetria.telemetria(tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4],tupla[i][5],tupla[i][6],tupla[i][7],tupla[i][8],tupla[i][9],tupla[i][10],tupla[i][11],tupla[i][12])
            telemetria1.set_id_telemetria(tupla[i][0])
            self.telemetrias.append(telemetria1)
        cursor.close()

    def insert_telemetria(self,id_dron, porcentaje_bateria, hora_actualizacion,latitud,longitud,altitud,cabeceo,guinada,alabeo,salud_camara,salud_gps,salud_controladora):
        res_rows= 0
        query="INSERT INTO Telemetria SET id_dron='"+id_dron+"', porcentaje_bateria='"+porcentaje_bateria+"',hora_actualizacion='"+hora_actualizacion+"',latitud='"+latitud+"',longitud='"+longitud+"',altitud='"+altitud+"',cabeceo='"+cabeceo+"',guinada='"+guinada+"',alabeo='"+alabeo+"',salud_camara='"+salud_camara+"',salud_gps='"+salud_gps+"',salud_controladora='"+salud_controladora+"'"
        cursor = self.connection.cursor()
        res_rows = cursor.execute(query)
        self.connection.commit()
        clase = telemetria.telemetria(id_dron, porcentaje_bateria, hora_actualizacion,latitud,longitud,altitud,cabeceo,guinada,alabeo,salud_camara,salud_gps,salud_controladora)
        self.telemetrias.append(clase)
        cursor.close()


        return res_rows

    def get_all_telemetria(self):
        self.telemetrias = []
        self.tupla = ()
        cursor = self.connection.cursor()
        query="select id_telemetria, id_dron, porcentaje_bateria, hora_actualizacion,latitud,longitud,altitud,cabeceo,guinada,alabeo,salud_camara,salud_gps,salud_controladora from Telemetria"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            telemetria_obj = telemetria.telemetria(tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4],tupla[i][5],tupla[i][6],tupla[i][7],tupla[i][8],tupla[i][9],tupla[i][10],tupla[i][11],tupla[i][12])
            telemetria_obj.set_id_telemetria(tupla[i][0])
            self.telemetrias.append(telemetria_obj)
        return self.telemetrias

    def delete_telemetria(self, telemetria):
        cursor = self.connection.cursor()
        query="delete from Foto where id_telemetria = '"+telemetria.get_telemetria()+"'"
        cursor.execute(query)
        self.connection.commit()