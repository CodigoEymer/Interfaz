#!/usr/bin/env python
import MySQLdb
import mision_dao_imp
import datetime as d

DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

all_users=[]

def create_mission():
    date=d.date.today()
    timestamp=d.datetime.now()
    insert_new_mission = prueba.insert_mission(
        "15", #id_usuario
        "Cali", #ciudad
        "Base aerea utilizada por la fuerza armada nacional", #descripcion
        "283500", #dimension
        "Cra 8 # 52-91", #direccion
        str(date), #fecha date:YYYY-MM-DD
        str(timestamp), #hora_inicio
        str(timestamp), #hora_fin
        "Prueba 2", #nombre_mision
        "Base Aerea Marco fidel Suarez", #nombre_ubicacion
        "2") #sobrelapamiento
        



if __name__ == "__main__":
    prueba = mision_dao_imp.mision_dao_imp(conn)
    #create_mission()