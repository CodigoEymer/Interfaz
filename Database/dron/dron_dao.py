#!/usr/bin/env python
import MySQLdb
import dron
import dbconnection

class dron_dao:
    def __init__(self, conn):
        self.connection = conn
        with self.connection.cursor() as cursor:
            query = "SELECT id_dron, id_mision, aceleracion_max, velocidad_max, altura_max, cvH, controladora, voltaje_inicial, tipo, cvV, hardware_id FROM Dron"
            cursor.execute(query)
            self.drones = [dron.dron(*row) for row in cursor.fetchall()]

    def insert_dron(self, dron):
        query = "INSERT INTO Dron (id_mision, aceleracion_max, velocidad_max, altura_max, cvH, controladora, voltaje_inicial, cvV, hardware_id, tipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        with self.connection.cursor() as cursor:
            res_rows = cursor.execute(query, (dron.get_id_mision(), dron.get_aceleracion_max(), dron.get_velocidad_max(), dron.get_altura_max(), dron.get_cvH(), dron.get_controladora(), dron.get_voltaje_inicial(), dron.get_cvV(), dron.get_hardware_id(), dron.get_tipo()))
            self.connection.commit()
        return res_rows

    def get_all_drones_mision(self, Id_mision):
        query = "SELECT id_dron, id_mision, aceleracion_max, velocidad_max, altura_max, cvH, controladora, voltaje_inicial, tipo, cvV, hardware_id FROM Dron WHERE id_mision = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (Id_mision,))
            self.drones = [dron.dron(*row) for row in cursor.fetchall()]
        return self.drones

    def get_dron(self, Id_mision, hardware_id):
        query = "SELECT id_dron, id_mision, aceleracion_max, velocidad_max, altura_max, cvH, controladora, voltaje_inicial, tipo, cvV, hardware_id FROM Dron WHERE id_mision = %s AND hardware_id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (Id_mision, hardware_id))
            row = cursor.fetchone()
            if row:
                return dron.dron(*row)
        return None

    def delete_dron(self, dron):
        query = "DELETE FROM Dron WHERE id_dron = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (dron.get_id_dron(),))
            self.connection.commit()