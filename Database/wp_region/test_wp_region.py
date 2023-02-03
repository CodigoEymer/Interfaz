#!/usr/bin/env python
import MySQLdb
import wp_region_dao_imp

DB_HOST = '127.0.0.1' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'drones' 

datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
conn = MySQLdb.connect(*datos)

all_users=[]

def create_wp_region():
    insert_new_wp_region = prueba.insert_wp_region(
        "7", #id_mision
        "3.4558632", #latitud_region
        "-76.5104336", #longitud_region
        "23", #altitud_region
    )


if __name__ == "__main__":
    prueba = wp_region_dao_imp.wp_region_dao_imp(conn)
    create_wp_region()