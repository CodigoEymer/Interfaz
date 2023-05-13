import json
import datetime as d
from Database.mision.mision_dao_imp import mision_dao_imp, mision, mision_dao
from Database.wp_region.wp_region_dao_imp import wp_region_dao_imp, wp_region, wp_region_dao
from Database.wp_recarga.wp_recarga_dao_imp import wp_recarga_dao_imp
from Database.dron.dron_dao_imp import dron_dao_imp
from Database.wp_dron.wp_dron_dao_imp import wp_dron_dao_imp
import MySQLdb
import Trayectorias
DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

id_mision = ""
id_dron = ""

class config_module():
    def __init__(self, id_usuario, ciudad, direccion, nombre_mision, nombre_rdi, descripcion, campo_de_vision, alt_maxima, vel_maxima, acc_maxima, sobrelapamiento, coordenadas,dimension,wp_recarga,controladora,voltaje_bateria,tipo):
        self.id_usuario = id_usuario
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
        self.controladora = controladora
        self.voltaje_bateria = voltaje_bateria
        self.tipo = tipo

    def insertar_mision(self):
        prueba = mision_dao_imp(conn)
        date=d.date.today()
        timestamp=d.datetime.now()
        hora_inicio = timestamp.strftime("%H:%M:%S")
        fecha=str(date)
        prueba.insert_mission(
            self.id_usuario, #id_usuario
            self.ciudad, #ciudad
            self.descripcion, #descripcion
            self.dimension, #dimension
            self.direccion, #direccion
            fecha, #fecha date:YYYY-MM-DD
            hora_inicio, #hora_inicio
            str(timestamp.strftime("%H:%M:%S")), #hora_fin
            self.nombre_mision, #nombre_mision
            self.nombre_rdi, #nombre_ubicacion
            self.sobrelapamiento) #sobrelapamiento
        
        global id_mision
        current_mission = prueba.get_mission(fecha,hora_inicio)
        id_mision = str(current_mission.get_id_mision())
    
    def calcular_autonomia(peso,potenciaXKg,voltaje_b,capacidad_b, seguridad,factor_seguridad):
        corriente_empuje = 1000*(peso*potenciaXKg)/voltaje_b

        autonomia_vuelo = capacidad_b*seguridad*60/(corriente_empuje*factor_seguridad)

        return autonomia_vuelo

    def generar_trayectoria(self):
        variables = Trayectorias.Trayectorias(self.coordenadas)
        #path = variables.ciclos()
        #print(variables.calcular_distancia_total())
        
        #return path
        return variables

    def insertar_wp_region(self):
        prueba = wp_region_dao_imp(conn)
        wp_list = self.coordenadas
        for wp in wp_list:
            prueba.insert_wp_region(id_mision,str(wp))

    def insertar_wp_recarga(self):
        wp_recarga = self.wp_recarga
        prueba = wp_recarga_dao_imp(conn)
        prueba.insert_wp_recarga(id_mision,wp_recarga)
        pass

    def insertar_dron(self):
        prueba = dron_dao_imp(conn)
        prueba.insert_dron(id_mision, self.acc_maxima, self.vel_maxima,self.alt_maxima, self.campo_de_vision,self.controladora,self.voltaje_bateria,self.tipo)
        global id_dron
        current_dron = prueba.get_dron(id_mision) 
        id_dron = str(current_dron.get_id_dron())

    def insertar_wp_dron(self,Vwp,h):
        prueba = wp_dron_dao_imp(conn)
        for wp_dron in Vwp:
            prueba.insert_wp_dron(id_dron,wp_dron[0],wp_dron[1],h)






