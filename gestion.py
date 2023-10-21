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

    def insertar_drones(self,id_mision,m_gen,alt):
        self.matriz_general = m_gen
        for i in range(len(self.dronV)):
            self.multi.insertar_dron(self.dronV[i],id_mision,self.matriz_general[i],alt)

    def completar_telemetrias(self, telemetriaV):
        idron = 0
        for telemetria in telemetriaV:
            telemetria.set_id_dron(self.dronV[idron].get_id_dron())
            print(self.dronV[idron].get_id_dron())
            idron = idron+1
            

    def coberturas(self,parent,wp_retorno_aut,progressBar_4,altura, ns):
        self.coberturas=[]
        c = 1
        for i in range(len(ns)):
            self.cobertura = Cobertura(parent,progressBar_4,float(altura)+c,float(altura), wp_retorno_aut[i],self.matriz_general[i],ns[i])
            c=c+2
            self.cobertura.StartMision()
            self.coberturas.append(self.cobertura)
    
    def definir_color(self):
        colores=[]
        for cobertura in self.coberturas:
            colores.append(cobertura.fcolorposse)
        return colores