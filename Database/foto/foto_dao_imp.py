#!/usr/bin/env python
import MySQLdb
import foto
import dbconnection

        
class foto_dao_imp:
    def __init__(self, conn):
        self.fotos = []
        self.tupla = ()
        self.connection = conn
        cursor = self.connection.cursor()
        query="select id_foto, id_dron, foto, hora_captura,latitud_captura,longitud_captura,altitud_captura from Foto"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            foto1 = foto.foto(tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4],tupla[i][5],tupla[i][6])
            foto1.set_id_foto(tupla[i][0])
            self.fotos.append(foto1)
        cursor.close()

    def insert_fotos(self,id_dron, photo, hora_captura,latitud_captura,longitud_captura,altitud_captura):
        res_rows= 0
        query="INSERT INTO Foto SET id_dron='"+id_dron+"', foto='"+photo+"',hora_captura='"+hora_captura+"',latitud_captura='"+latitud_captura+"',longitud_captura='"+longitud_captura+"',altitud_captura='"+altitud_captura+"'"
        cursor = self.connection.cursor()
        res_rows = cursor.execute(query)
        self.connection.commit()
        clase = foto.foto(id_dron, photo, hora_captura,latitud_captura,longitud_captura,altitud_captura)
        self.fotos.append(clase)
        cursor.close()
        return res_rows
    
    def insert_bash(self,fotos):
        cursor = self.connection.cursor()
        query="INSERT INTO Telemetria(id_foto, id_dron, foto, hora_captura, latitud_captura, longitud_captura, altitud_captura) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        datos = []
        for foto in fotos:
            dato = [foto.get_id_foto(), foto.get_id_dron(), foto.get_foto(),foto.get_hora_captura(),foto.get_latitud_captura(),foto.get_longitud_captura(),foto.get_altitud_captura()]

        try:
            cursor.executemany(query, datos)          
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print("error",e)
            self.connection.rollback()

    def insert_batch(self,fotos):
        cursor = self.connection.cursor()
        query="INSERT INTO Foto( id_dron, foto, hora_captura, latitud_captura, longitud_captura, altitud_captura) VALUES (%s,%s,%s,%s,%s,%s)"

        datos = []
        for foto in fotos:
            dato = [foto.get_id_dron(), foto.get_foto(),foto.get_hora_captura(),foto.get_latitud_captura(),foto.get_longitud_captura(),foto.get_altitud_captura()]
            datos.append(dato)

        try:
            cursor.executemany(query, datos)          
            self.connection.commit()
            cursor.close()
            
        except Exception as e:
            self.connection.rollback()

    def get_all_fotos(self):
        self.fotos = []
        self.tupla = ()
        cursor = self.connection.cursor()
        query="select id_foto, id_dron, foto, hora_captura,latitud_captura,longitud_captura,altitud_captura from Foto"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            foto1 = foto.foto(tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4],tupla[i][5],tupla[i][6])
            foto1.set_id_foto(tupla[i][0])
            self.fotos.append(foto1)
        cursor.close()
        return self.fotos

    def delete_foto(self, foto):
        cursor = self.connection.cursor()
        query="delete from Foto where id_foto = '"+foto.get_id_foto()+"'"
        cursor.execute(query)
        self.connection.commit()