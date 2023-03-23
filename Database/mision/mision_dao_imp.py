#!/usr/bin/env python
import MySQLdb
import mision
import mision_dao

class mision_dao_imp():

    def __init__(self, conn):
        self.missions = []
        self.tupla = ()
        self.connection = conn
        cursor = self.connection.cursor()
        query="select id_mision, id_usuario, ciudad, descripcion, dimension, direccion, fecha, hora_inicio, hora_fin, nombre_mision, nombre_ubicacion, sobrelapamiento from Mision"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            mission = mision.mision(tupla[i][0],tupla[i][1],tupla[i][2],tupla[i][3], tupla[i][4], tupla[i][5], tupla[i][6], tupla[i][7], tupla[i][8], tupla[i][9], tupla[i][10], tupla[i][11])
            self.missions.append(mission)
        cursor.close()

    def get_mission(self,fecha, hora_inicio):
        res_mission= None
        query="select id_mision, id_usuario, ciudad, descripcion, dimension, direccion, fecha, hora_fin, nombre_mision, nombre_ubicacion, sobrelapamiento from Mision where hora_inicio= '" + str(hora_inicio)+"' AND fecha='" + str(fecha)+"'"
        try:
            cursor = self.connection.cursor()
            result = cursor.execute(query)
            tupla = cursor.fetchone()
            res_mission = mision.mision(tupla[0],tupla[1],tupla[2],tupla[3], tupla[4], tupla[5], tupla[6], hora_inicio, tupla[7], tupla[8], tupla[9], tupla[10])
        except Exception as e: print(e)
        cursor.close()
        
        return res_mission
    
    def get_all_missions_xUser(self,idUsuario):
        self.missions = []
        cursor = self.connection.cursor()
        query="select id_mision, id_usuario, ciudad, descripcion, dimension, direccion, fecha, hora_inicio, hora_fin, nombre_mision, nombre_ubicacion, sobrelapamiento from Mision where id_usuario= '" + str(idUsuario)+"'"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            mission = mision.mision(tupla[i][0],tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4],tupla[i][5],tupla[i][6],tupla[i][7],tupla[i][8],tupla[i][9],tupla[i][10],tupla[i][11])       
            self.missions.append(mission)
        cursor.close()
        return self.missions

    def get_all_missions_xUserANDciudad(self,idUsuario,ciudad):
        self.missions = []
        cursor = self.connection.cursor()
        query="select id_mision, id_usuario, ciudad, descripcion, dimension, direccion, fecha, hora_inicio, hora_fin, nombre_mision, nombre_ubicacion, sobrelapamiento from Mision where id_usuario= '" + str(idUsuario)+"' AND ciudad='" + str(ciudad)+"'"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            mission = mision.mision(tupla[i][0],tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4],tupla[i][5],tupla[i][6],tupla[i][7],tupla[i][8],tupla[i][9],tupla[i][10],tupla[i][11]) 
            #print([i][1])       
            self.missions.append(mission)
        cursor.close()
        return self.missions

    def get_all_missions_xUserANDciudadANDname(self,idUsuario,ciudad,name_mision):
        self.missions = []
        cursor = self.connection.cursor()
        query="select id_mision, id_usuario, ciudad, descripcion, dimension, direccion, fecha, hora_inicio, hora_fin, nombre_mision, nombre_ubicacion, sobrelapamiento from Mision where id_usuario= '" + str(idUsuario)+"' AND ciudad='" + str(ciudad)+"' AND nombre_mision='" + str(name_mision)+"'"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            mission = mision.mision(tupla[i][0],tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4],tupla[i][5],tupla[i][6],str(tupla[i][7]),tupla[i][8],tupla[i][9],tupla[i][10],tupla[i][11])   
            self.missions.append(mission)
        cursor.close()
        return self.missions

    def insert_mission(self, id_usuario, ciudad, descripcion, dimension, direccion, fecha, hora_inicio, hora_fin, nombre_mision,nombre_ubicacion,sobrelapamiento):
        res_rows= 0
        query="INSERT INTO Mision SET id_usuario='"+id_usuario+"', ciudad='"+ciudad+"', descripcion='"+descripcion+"', dimension='"+dimension+"',direccion='"+direccion+"', fecha='"+fecha+"',hora_inicio='"+hora_inicio+"', hora_fin='"+hora_fin+"', nombre_mision='"+nombre_mision+"',nombre_ubicacion='"+nombre_ubicacion+"',sobrelapamiento='"+sobrelapamiento+"'"
        cursor = self.connection.cursor()
        res_rows = cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return res_rows

    def get_all_missions(self):
        self.missions = []
        cursor = self.connection.cursor()
        query="select id_mision, id_usuario, ciudad, descripcion, dimension, direccion, fecha, hora_inicio, hora_fin, nombre_mision, nombre_ubicacion, sobrelapamiento from Mision"
        cursor.execute(query)
        tupla = cursor.fetchall()
        n_filas = len(tupla)
        for i in range(n_filas):
            mission = mision.mision(tupla[i][0],tupla[i][1],tupla[i][2],tupla[i][3],tupla[i][4],tupla[i][5],tupla[i][6],tupla[i][7],tupla[i][8],tupla[i][9],tupla[i][10],tupla[i][11])
            
            self.missions.append(mission)
        cursor.close()
        return self.missions
    

    def update_mission(self, mission):
        cursor = self.connection.cursor()
        query="update Mision set ciudad='"+mission.get_ciudad()+"', descripcion='"+mission.get_descripcion()+"', dimension='"+mission.get_dimension()+"',direccion='"+mission.get_direccion()+"',fecha='"+mission.fecha()+"',hora_inicio='"+mission.hora_inicio()+"',hora_fin='"+mission.hora_fin()+"',id_mision='"+mission.id_mision()+"',id_usuario='"+mission.id_usuario()+"',nombre_mision='"+mission.nombre_mision()+"',nombre_ubicacion='"+mission.nombre_ubicacion()+"',sobrelapamiento='"+mission.sobrelapamiento()+"' where id_mision = 6"
        cursor.execute(query)
        self.connection.commit()

    def update_fecha_fin(self, id_mission):
        pass


    def delete_mission(self, mission):
        cursor = self.connection.cursor()
        query="delete from Mision where mision_id = '"+mission.get_id_mision+"'"
        cursor.execute(query)
        self.connection.commit()