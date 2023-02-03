#!/usr/bin/env python
import MySQLdb
import dron_dao_imp
import dron

DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

all_users=[]

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

def create_dron():

    insert_new_user = prueba.insert_dron(
    "7",    #id_mision
    "5",    #aceleracion_max
    "10",    #velocidad_max
    "160",    #altura_max
    "90",    #campo_vision
    "Pixhak",    #controladora
    "25",    #duracion_bateria
    "cuadricoptero")    #tipo
    #get_user_by_id = prueba.get_user(12)
    #print(get_user_by_id.get_correo())

def get_all_drones():
    #Obtener todos los usuarios
    all_users=prueba.get_all_drones()
    print("Drones")
    for item in all_users:
        print(str(item.get_id_mision())+","+str(item.get_controladora()))

def uptate_user():
    get_user_by_id = prueba.get_user(6)
    get_user_by_id.set_nombre_usuario("Jorge")
    user_updated = prueba.update_user(get_user_by_id)

def delete_user():
    get_user_by_id = prueba.get_user(12)
    prueba.delete_user(get_user_by_id)

if __name__ == "__main__":
    prueba = dron_dao_imp.dron_dao_imp(conn)
    #create_dron()
    #uptate_user()
    #delete_user()
    get_all_drones()
