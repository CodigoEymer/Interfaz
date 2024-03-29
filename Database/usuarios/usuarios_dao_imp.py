#!/usr/bin/env python
import MySQLdb
import usuarios
import usuarios_dao

        
class usuarios_dao_imp:
    def __init__(self, conn):
        self.users = []
        self.tupla = ()
        self.connection = conn
        cursor = self.connection.cursor()
        query="select id_usuario,nombre, nombre_usuario, correo, celular from Usuario"
        cursor.execute(query)
        #result = conn.store_result()
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            user = usuarios.usuarios(tupla[i][0],tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4])
            self.users.append(user)
        cursor.close()

    def get_user(self, id_usuario):
        res_user= None
        query="select nombre, nombre_usuario, correo, celular from Usuario where id_usuario=" + str(id_usuario)
        print(query)
        try:
            cursor = self.connection.cursor()
            result = cursor.execute(query)
            tupla1 = cursor.fetchone()
            res_user = usuarios.usuarios(str(id_usuario),tupla1[0],tupla1[1],tupla1[2],tupla1[3])
        except Exception as e: print(e)
        cursor.close()
        return res_user

    def insert_user(self, nombre, nombre_usuario, correo, celular):
        res_rows= 0
        query="INSERT INTO Usuario SET nombre='"+nombre+"', nombre_usuario='"+nombre_usuario+"', correo='"+correo+"',celular='"+celular+"'"
 
        cursor = self.connection.cursor()
        res_rows = cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return res_rows

    def get_all_users(self):
        self.users = []
        cursor = self.connection.cursor()
        query="select id_usuario,nombre, nombre_usuario, correo, celular from Usuario"
        cursor.execute(query)
        #result = conn.store_result()
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            user = usuarios.usuarios(tupla[i][0],tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4])
            self.users.append(user)
        cursor.close()
        return self.users

    def update_user(self, id_user,nombre, nombre_usuario, correo, celular):
        cursor = self.connection.cursor()
        query = """
        UPDATE Usuario
        SET nombre = %s, nombre_usuario = %s, correo = %s, celular = %s
        WHERE id_usuario = %s
        """
        values = (nombre, nombre_usuario, correo, celular, id_user)
        cursor.execute(query, values)
        self.connection.commit()

    def delete_user(self, user):
        cursor = self.connection.cursor()
        query="delete from Usuario where nombre_usuario = '"+user.get_nombre_usuario()+"'"
        cursor.execute(query)
        self.connection.commit()

    def get_usuario(self,nombre_usuario):
        res_mission= None
        query="select id_usuario,nombre, nombre_usuario, correo, celular from Usuario where nombre_usuario= '" + str(nombre_usuario)+"'"
        try:
            cursor = self.connection.cursor()
            result = cursor.execute(query)
            tupla = cursor.fetchone()
            user = usuarios.usuarios(tupla[0],tupla[1],tupla[2],tupla[3], tupla[4])
        except Exception as e: print(e)
        cursor.close()
        
        return user