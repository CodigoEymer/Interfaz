from config_module import multi_config_module
from Cobertura import Cobertura
class Gestion():
    def __init__(self,dronV):
        self.multi = multi_config_module()
        self.dronV = dronV


    def set_user_values(self,max_acce,max_speed,max_height,cvh,cvv):
        for dron in self.dronV:

            dron.set_aceleracion_max(max_acce)
            dron.set_velocidad_max(max_speed)
            dron.set_altura_max(max_height)
            dron.set_cvH(cvh)
            dron.set_cvV(cvv)

    def insertar_drones(self,id_mision):
        for dron in self.dronV:
            self.multi.insertar_dron(dron,id_mision)

    def completar_telemetrias(self, telemetriaV):
        idron = 0
        for telemetria in telemetriaV:
            telemetria.set_id_dron(self.dronV[idron].get_id_dron())
            idron = idron+1

    def wp_retorno_home(self,matriz_wp_drones, distancia_wp_retorno, trayectorias):
        self.matriz_general = []
        for wps in matriz_wp_drones:
            self.wp_retorno_aut = trayectorias.calcular_wp_distancia(wps,distancia_wp_retorno)
            self.wp_tramos = trayectorias.get_tramos() 
            self.matriz_general.append(self.wp_tramos)
        return self.matriz_general
    
    def insertar_wp_drones(self,max_height):
        for wp_dron in self.matriz_general:
            self.multi.insertar_wp_dron(wp_dron,max_height)

    def coberturas(self,parent,lista_wp,progressBar_4,altura, wp_retorno_aut,finish_mission, ns):
        for i in range(len(ns)):
            cobertura = Cobertura(parent,lista_wp,progressBar_4,altura, wp_retorno_aut,self.matriz_general[i],finish_mission,ns[i])
            cobertura.StartMision()


    
