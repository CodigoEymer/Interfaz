#!/usr/bin/env python
import MySQLdb
import telemetria
import dbconnection

        
class telemetria_dao_imp:
    def __init__(self, conn):
        self.connection = conn

    def insert_bash(self,v_telemetria):
        cursor = self.connection.cursor()
        query="INSERT INTO Telemetria(id_dron, porcentaje_bateria, salud_gps, salud_controladora, salud_bateria, salud_motores, salud_imu, hora_actualizacion, latitud, longitud, altitud, cabeceo, guinada, alabeo, salud_camara) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        datos = []
        for telemetria in v_telemetria:
            dato = [telemetria.get_id_dron(), telemetria.get_porcentaje_bateria(), telemetria.get_salud_gps(),telemetria.get_salud_controladora(),telemetria.get_salud_bateria(),telemetria.get_salud_motores(),telemetria.get_salud_imu(),telemetria.get_hora_actualizacion(),telemetria.get_latitud(),telemetria.get_longitud(),telemetria.get_altitud(),telemetria.get_cabeceo(),telemetria.get_guinada(),telemetria.get_alabeo(),telemetria.get_salud_camara()]
            datos.append(dato)

        try:
            cursor.executemany(query, datos)          
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print("error",e)
            self.connection.rollback()

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