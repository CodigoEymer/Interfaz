import math
import ast

class Trayectorias():
    def __init__(self,coords):
        #input
        self.coords = str(coords)
        self.coords.replace("[","(")
        self.coords.replace("]",")")
        self.coords="["+self.coords[1:-1]+"]"
        self.vertices_global = ast.literal_eval(self.coords)
        self.vertices=[]
        for punto in self.vertices_global:
            x,y=self.to_cartesian(punto[1],punto[0])
            self.vertices.append((x,y))
        #output
        self.wp_dron =[] 
        # Campo de vision
        self.LX = 1.0/20
        self.LY = 1.0/20
        # Sobrelapamiento minimo en Y
        self.Ovx = 0.1/20
        # Distancia entre vertices
        self.di = 0

        self.p = len(self.vertices)

        #Encuentra la apotema minima a partir del centroide
        self.apotema()

       # Distancia entre anillos
        self.dr = self.LX-self.Ovx

        # Numero de anillos
        self.nr = (self.dcp-self.Ovx)/self.dr
        self.num_rings = int(math.ceil(self.nr))


        
        if self.num_rings==1:
            self.Ovx = 0.0
        else:
            #Ovx recalculado
            self.Ovx=(self.num_rings*self.LX-self.dcp)/(self.num_rings-1)
            #dr recalculado
            self.dr=(self.dcp-self.LX)/(self.num_rings-1)
         

    def to_cartesian(self, latitude, longitude):
        # Convertir a radianes
        lat_rad = math.radians(latitude)
        long_rad = math.radians(longitude)

        # Constantes
        R = 6371000  # Radio de la Tierra en metros

        # Proyeccion de Mercator
        x = R * long_rad
        y = R * math.log(math.tan(math.pi/4 + lat_rad/2))

        # Convertir a kilometros
        x_km = x / 1000
        y_km = y / 1000

        return x_km, y_km

    def to_geographic(self, x_km, y_km):
        # Convertir a metros
        x_m = x_km * 1000
        y_m = y_km * 1000

        # Constantes
        R = 6371000  # Radio de la Tierra en metros

        # Proyeccion inversa de Mercator
        longitude = math.degrees(x_m / R)
        latitude = math.degrees(2 * math.atan(math.exp(y_m / R)) - math.pi/2)

        return latitude, longitude

    def distancia(self, x1, y1, x2, y2):
        r= math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return r

    def angle_between_vectors(self, x1, y1, x2, y2):
        dot_product = x1 * x2 + y1 * y2
        mag_product = math.sqrt(x1**2 + y1**2) * math.sqrt(x2**2 + y2**2)

        if y2<0:
            tetha= -(math.acos(dot_product/mag_product))
        else:
            tetha= (math.acos(dot_product/mag_product))
        return (tetha)

    def apotema(self):
        sum_x = sum([v[0] for v in self.vertices])
        sum_y = sum([v[1] for v in self.vertices])
        centroid_x = sum_x / self.p
        centroid_y = sum_y / self.p
        cp=(centroid_x,centroid_y)
        self.dcp = float("inf")
        for m in range(self.p): 
            x1, y1 = self.vertices[m]
            x2, y2 = self.vertices[(m + 1) % self.p]
            dx = x2 - x1
            dy = y2 - y1
            distance = abs(dx * (centroid_y - y1) - dy * (centroid_x - x1)) / math.sqrt(dx**2 + dy**2)
            if distance < self.dcp:
                self.dcp = distance

    def intersection_point(self, p1, p2, p3, p4):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4

        # Compute slopes and y-intercepts of each line
        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1 * x1
        m2 = (y4 - y3) / (x4 - x3)
        b2 = y3 - m2 * x3

        # Compute x and y coordinates of intersection point
        x_intersect = (b2 - b1) / (m1 - m2)
        y_intersect = m1 * x_intersect + b1
        #print("Interseccion: "+str(x_intersect)+", "+str(y_intersect))
        return x_intersect, y_intersect
    
    def findUpperPoints(self, centroid, x, y, theta):
        x0,y0 = centroid
        # Convertir el angulo de grados a radianes
        #theta = math.radians(theta)

        # Calcular las coordenadas del punto rotado
        x_rotated = (x - x0) * math.cos(theta) - (y - y0) * math.sin(theta) + x0
        y_rotated = (x - x0) * math.sin(theta) + (y - y0) * math.cos(theta) + y0
        #print("Punto: "+str(x_rotated)+", "+str(y_rotated))
        return (x_rotated, y_rotated)

    def ciclos(self):
        new_vertices = self.vertices
        for j in range(self.num_rings):
            self.vertices = new_vertices
            new_vertices = []
            #print("Vertices: "+str(self.vertices))
            #Actualizar p?
            for i in range(self.p):
                x0, y0 = self.vertices[i-1]
                if i == self.p-1:
                    x1, y1 = self.vertices[-1]
                else:
                    x1, y1 = self.vertices[i]
                if i == self.p-1:
                    x2, y2 = self.vertices[0]
                elif i == self.p-2:
                    x2, y2 = self.vertices[-1]
                else:
                    x2, y2 = self.vertices[i+1]
                vector1x = float(x0 - x1)
                vector1y = float(y0 - y1)
                vector2x = float(x2 - x1)
                vector2y = float(y2 - y1)
                angleY = self.angle_between_vectors(vector1x, vector1y, vector2x, vector2y)
                
                if i == 0 and j == 0:    
                    di = self.distancia(x1, y1, x2, y2)-(self.LX/(math.tan(angleY)))      
                else:
                    di = self.distancia(x1, y1, x2, y2)

                # Sobrelapamiento minimo en Y [m]
                Ovy = 0.1/20

                # Distancia entre weypoints [m]
                dw = self.LY-Ovy

                # Numero de waypoints
                nw = (di-Ovy)/dw
                num_wp_line = int(math.ceil(nw))

                if num_wp_line==1:
                    Ovy = 0.0
                else:
                    # Ovy recalculado  
                    Ovy = (num_wp_line*self.LY-di)/(num_wp_line-1)
                    # dw recalculado
                    dw = (di-self.LY)/(num_wp_line-1)

                dx = float(x2 - x1)
                dy = float(y2 - y1)
                
                angulo = self.angle_between_vectors(1.0, 0.0, dx, dy)
                catetox = math.cos(angulo)*dw
                catetoy = math.sin(angulo)*dw

                for k in range(num_wp_line):
                    if k == 0:
                        h = math.sqrt((self.LX/2)**2 + (self.LY/2)**2)
                        angulo_phi = math.atan(self.LX/self.LY)
                        angulo_alpha = angulo_phi + angulo
                        if i == 0 and j == 0:   
                            if dx == 0:
                                catetoxO = 0
                                catetoyO = dw
                            else:  
                                catetoxO = math.cos(angulo)*(self.LX/math.tan(angleY))
                                catetoyO = math.sin(angulo)*(self.LX/math.tan(angleY))
                            self.wp_dron.append(((x1+catetoxO)+h*math.cos(angulo_alpha),(y1+catetoyO)+h*math.sin(angulo_alpha)))
                            x_0, y_0 = self.wp_dron[0]
                            x_1 = x_0 - self.LX/2
                            y_1 = y_0 + self.LY/2
                            px2,py2 = self.findUpperPoints((x_0,y_0),x_1,y_1,angulo)
                            new_vertices.append((px2,py2))
                        else:
                            indice=  (len(self.wp_dron))-1
                            self.wp_dron.append((x1+h*math.cos(angulo_alpha),y1+h*math.sin(angulo_alpha)))
                            x_0, y_0 = self.wp_dron[indice+1]

                            x_1 = x_0 - self.LX/2
                            y_1 = y_0 + self.LY/2
                            p3 = self.findUpperPoints((x_0,y_0),x_1,y_1,angulo)

                            x_2 = x_0 + self.LX/2
                            y_2 = y_0 + self.LY/2
                            p4 = self.findUpperPoints((x_0,y_0),x_2,y_2,angulo)

                            punto = self.intersection_point(p1, p2, p3, p4)
                            new_vertices.append(punto)

                    else:
                        indice=  (len(self.wp_dron))-1
                        xwp , ywp = self.wp_dron[indice]
                        self.wp_dron.append((xwp+catetox,ywp+catetoy))
                        if k == (num_wp_line-1):
                            x_0, y_0 = self.wp_dron[indice+1]

                            x_1 = x_0 - self.LX/2
                            y_1 = y_0 + self.LY/2
                            p1 = self.findUpperPoints((x_0,y_0),x_1,y_1,angulo)

                            x_2 = x_0 + self.LX/2
                            y_2 = y_0 + self.LY/2
                            p2 = self.findUpperPoints((x_0,y_0),x_2,y_2,angulo)
        
        wp_dron_global=[]
        for punto in self.wp_dron:
            lat,long=self.to_geographic(punto[0],punto[1])
            wp_dron_global.append((lat,long))

        return wp_dron_global
        

        
        

 