import json
import datetime as d
from Database.mision.mision_dao_imp import mision_dao_imp, mision, mision_dao

import MySQLdb
DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

class config_module():
    def __init__(self, ciudad, direccion, nombre_mision, nombre_rdi, descripcion, campo_de_vision, alt_maxima, vel_maxima, acc_maxima, sobrelapamiento, coordenadas,dimension,wp_recarga):

        self.ciudad = ciudad
        self.direccion = direccion
        self.nombre_mision = nombre_mision
        self.nombre_rdi = nombre_rdi
        self.descripcion = descripcion
        self.campo_de_vision = campo_de_vision
        self.alt_maxima = alt_maxima
        self.vel_maxima = vel_maxima
        self.acc_maxima = acc_maxima
        self.sobrelapamiento = sobrelapamiento
        self.coordenadas = coordenadas
        self.dimension = dimension
        self.wp_recarga = wp_recarga

        #self.insertar_mision()

    def insertar_mision(self):
        prueba = mision_dao_imp(conn)
        date=d.date.today()
        timestamp=d.datetime.now()

        prueba.insert_mission(
            "15", #id_usuario
            self.ciudad, #ciudad
            self.descripcion, #descripcion
            self.dimension, #dimension
            self.direccion, #direccion
            str(date), #fecha date:YYYY-MM-DD
            str(timestamp), #hora_inicio
            str(timestamp), #hora_fin
            self.nombre_mision, #nombre_mision
            self.nombre_rdi, #nombre_ubicacion
            self.sobrelapamiento) #sobrelapamiento
        
        All_Mission =  prueba.get_all_missions()
        for mision in All_Mission:
            print(str(mision.get_id_mision()))
    
    def calcular_autonomia():
        pass
    
    def insertar_dron():
        pass

    def insertar_wp_region():
        pass

    def insertar_wp_recarga():
        pass

    def insertar_wp_dron():
        pass



