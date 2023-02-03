#!/usr/bin/env python
import MySQLdb
import telemetria_dao_imp
import telemetria

DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

all_telemetrias=[]

def run_query(query=''):
    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 

    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select 
    else: 
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
    
    cursor.close()
    conn.close()

    return data

def create():

    insert_new_user = prueba.insert_telemetria(
    "3",                #id_dron
    "95",               #porcentaje_bateria
    "16:03:00",         #hora_actualizacion
    "-76.506421",           #latitud
    "3.455063",           #longitud
    "8",                #altitud
    "90",               #cabeceo
    "70",               #guinada
    "30",               #alabeo
    "1",                #salud_camara
    "1",                #salud_gps
    "1")                #salud_controladora

    #get_user_by_id = prueba.get_user(12)
    #print(get_user_by_id.get_correo())

def get_all():
    #Obtener todos los usuarios
    all_items=prueba.get_all_telemetria()
    print("telemetrias")
    for item in all_items:
        print(str(item.get_id_dron())+","+str(item.get_id_telemetria()))

def uptate():
    get_user_by_id = prueba.get_user(6)
    get_user_by_id.set_nombre_usuario("Jorge")
    user_updated = prueba.update_user(get_user_by_id)

def delete():
    id_telemetria = 1
    prueba.delete_telemetria(id_telemetria)

if __name__ == "__main__":
    prueba = telemetria_dao_imp.telemetria_dao_imp(conn)
    create()
    #uptate_user()
    #delete_user()
    get_all()
