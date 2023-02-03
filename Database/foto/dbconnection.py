#!/usr/bin/env python
import MySQLdb
import foto_dao_imp
import foto
import datetime as d

DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

all_fotos=[]

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
    timestamp=d.datetime.now()
    insert_new_photo = prueba.insert_foto(
    "3",                #id_dron
    "archivo.png",      #foto
    str(timestamp),     #hora_captura
    "-76.506421",       #latitud_captura
    "3.455063",           #longitud_captura
    "10.23")                #altitud_captura

    #get_user_by_id = prueba.get_user(12)
    #print(get_user_by_id.get_correo())

def get_all():
    #Obtener todos los usuarios
    all_items=prueba.get_all_fotos()
    print("Fotos")
    for item in all_items:
        print(str(item.get_id_foto())+","+str(item.get_foto()))

def uptate():
    get_user_by_id = prueba.get_user(6)
    get_user_by_id.set_nombre_usuario("Jorge")
    user_updated = prueba.update_user(get_user_by_id)

def delete():
    id_foto = 1
    prueba.delete_foto(id_foto)

if __name__ == "__main__":
    prueba = foto_dao_imp.foto_dao_imp(conn)
    create()
    #uptate_user()
    #delete_user()
    get_all()
