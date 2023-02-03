#!/usr/bin/env python
import MySQLdb
import wp_dron_dao_imp

DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

all_users=[]

def create_wp_dron():
    insert_new_wp_dron = prueba.insert_wp_dron(
        "3", #id_dron
        "3.4544421", #latitud_ruta
        "-76.5099507", #longitud_ruta
        "8", #altitud_ruta
    )


if __name__ == "__main__":
    prueba = wp_dron_dao_imp.wp_dron_dao_imp(conn)
    create_wp_dron()