#!/usr/bin/env python
import MySQLdb
import dron
import dbconnection

        
class dron_dao_imp:
    def __init__(self, conn):
        self.drones = []
        self.tupla = ()
        self.connection = conn
        cursor = self.connection.cursor()
        query="select id_dron, id_mision, aceleracion_max, velocidad_max,altura_max, campo_vision,controladora,duracion_bateria,tipo from Dron"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            user = dron.dron(tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4],tupla[i][5],tupla[i][6],tupla[i][7],tupla[i][8])
            user.set_id_dron(tupla[i][0])
            self.drones.append(user)
        cursor.close()

    def insert_dron(self,id_mision, aceleracion_max, velocidad_max,altura_max, campo_vision,controladora,duracion_bateria,tipo):
        res_rows= 0
        query="INSERT INTO Dron SET id_mision='"+id_mision+"', aceleracion_max='"+aceleracion_max+"',velocidad_max='"+velocidad_max+"',altura_max='"+altura_max+"',campo_vision='"+campo_vision+"',controladora='"+controladora+"',duracion_bateria='"+duracion_bateria+"', tipo='"+tipo+"'"
        print(query)
        cursor = self.connection.cursor()
        res_rows = cursor.execute(query)
        self.connection.commit()
        res_user = dron.dron(id_mision, aceleracion_max, velocidad_max,altura_max,campo_vision,controladora,duracion_bateria,tipo)
        self.drones.append(res_user)
        cursor.close()
        return res_rows

    def get_all_drones(self):
        self.drones = []
        cursor = self.connection.cursor()
        query="select id_dron, id_mision, aceleracion_max, velocidad_max,altura_max, campo_vision,controladora,duracion_bateria,tipo from Dron"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            user = dron.dron(tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4],tupla[i][5],tupla[i][6],tupla[i][7],tupla[i][8])
            self.drones.append(user)
        cursor.close()
        return self.drones

    def delete_dron(self, dron):
        cursor = self.connection.cursor()
        query="delete from Dron where id_dron = '"+dron.get_id_dron()+"'"
        cursor.execute(query)
        self.connection.commit()