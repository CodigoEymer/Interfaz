import json
import datetime as d
from Database.mision.mision_dao_imp import mision_dao_imp, mision, mision_dao
from Database.wp_region.wp_region_dao_imp import wp_region_dao_imp, wp_region, wp_region_dao
from Database.wp_recarga.wp_recarga_dao_imp import wp_recarga_dao_imp
from Database.dron.dron_dao_imp import dron_dao_imp
from Database.wp_dron.wp_dron_dao_imp import wp_dron_dao_imp
from Database.telemetria.telemetria_dao_imp import telemetria_dao_imp
import MySQLdb
import Trayectorias

DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

class config_module():  
    def __init__(self, id_usuario = "", ciudad = "", direccion = "", nombre_mision = "", nombre_ubicacion = "", descripcion = "", sobrelapamiento = "", coordenadas = "",dimension = "",wp_recarga = "",dron= None):
        self.id_mision = ""
        self.id_dron = ""
        self.id_usuario = id_usuario
        self.ciudad = ciudad
        self.direccion = direccion
        self.nombre_mision = nombre_mision
        self.nombre_ubicacion = nombre_ubicacion
        self.descripcion = descripcion
        self.sobrelapamiento = sobrelapamiento
        self.coordenadas = coordenadas
        self.dimension = dimension
        self.wp_recarga = wp_recarga
        self.dron = dron


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
            self.nombre_ubicacion, #nombre_ubicacion
            self.sobrelapamiento) #sobrelapamiento
        
        current_mission = prueba.get_mission(fecha,hora_inicio)
        self.id_mision = str(current_mission.get_id_mision())


    def insertar_wp_region(self):
        prueba = wp_region_dao_imp(conn)
        wp_list = self.coordenadas
        for wp in wp_list:
            prueba.insert_wp_region(self.id_mision,str(wp))

    def insertar_wp_recarga(self):
        wp_recarga = self.wp_recarga
        prueba = wp_recarga_dao_imp(conn)
        prueba.insert_wp_recarga(self.id_mision,wp_recarga)
        pass

    def insertar_dron(self):
        prueba = dron_dao_imp(conn)
        self.dron.set_id_mision(self.id_mision)
        prueba.insert_dron(self.dron)
        current_dron = prueba.get_dron(self.id_mision) 
        self.id_dron = str(current_dron.get_id_dron())
        self.dron.set_id_dron(self.id_dron)

    def insertar_telemetria(self,v_telemetria):
        prueba = telemetria_dao_imp(conn)
        prueba.insert_bash(v_telemetria)


    def insertar_wp_dron(self,Vwp,h):
        prueba = wp_dron_dao_imp(conn)
        for wp_dron in Vwp:
            prueba.insert_wp_dron(self.id_dron,wp_dron[0],wp_dron[1],h)


    def calcular_autonomia(self,peso,potenciaXKg,voltaje_b,capacidad_b, seguridad,factor_seguridad,velocidad):
        corriente_empuje = 1000*(peso*potenciaXKg)/voltaje_b
        autonomia_vuelo = capacidad_b*seguridad*60/(corriente_empuje*factor_seguridad)
        dwr = autonomia_vuelo*60*velocidad/1000

        return dwr

    def generar_trayectoria(self):
        variables = Trayectorias.Trayectorias(self.coordenadas,float(self.dron.get_altura_max()), float(self.dron.get_cvH()),float(self.dron.get_cvV()),float(self.sobrelapamiento))
        return variables

    def getParameters(self):
        velocidad_cm = int(self.dron.get_velocidad_max())*100
        parameters = [self.dron.get_aceleracion_max(), velocidad_cm]
        return parameters