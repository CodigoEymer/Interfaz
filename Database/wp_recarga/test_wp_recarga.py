#!/usr/bin/env python
import MySQLdb
import wp_recarga_dao_imp

DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

all_users=[]

def create_wp_recarga():
    insert_new_wp_recarga = prueba.insert_wp_recarga(
        "7", #id_mision
        "3.4533127", #latitud_recarga
        "-76.5124245", #longitud_recarga
        "1", #altitud_recarga
    )


if __name__ == "__main__":
    prueba = wp_recarga_dao_imp.wp_recarga_dao_imp(conn)
    create_wp_recarga()