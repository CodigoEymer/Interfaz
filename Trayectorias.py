import math

vertices = [(6,4), (12,4), (12,10), (6,10)]
# Campo de vision
LX = 1.0
LY = 1.0
# Sobrelapamiento minimo en X y Y
Ovx = 0.1
Ovy = 0.1
# Distancia entre anillos
dr = LX-Ovx
# Distancia entre weypoints
dw = LY-Ovy
# Distancia entre vertices
di = 0

p = len(vertices)
sum_x = sum([v[0] for v in vertices])
sum_y = sum([v[1] for v in vertices])
centroid_x = sum_x / p
centroid_y = sum_y / p

def distancia(x1, y1, x2, y2):
    r= math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return r

def angle_between_vectors(x1, y1, x2, y2):
    dot_product = x1 * x2 + y1 * y2
    mag_product = math.sqrt(x1**2 + y1**2) * math.sqrt(x2**2 + y2**2)
    return math.degrees(math.acos(dot_product/mag_product))

print("Centroid: "+str(centroid_x)+","+str(centroid_y))

dcp = float("inf")

wp_dron =[]

for m in range(p): 

    x1, y1 = vertices[m]
    x2, y2 = vertices[(m + 1) % p]
    dx = x2 - x1
    dy = y2 - y1
    distance = abs(dx * (centroid_y - y1) - dy * (centroid_x - x1)) / math.sqrt(dx**2 + dy**2)

    if distance < dcp:
        dcp = distance

print("La apotema del poligono es:", dcp)

# Numero de anillos
nr = (dcp-Ovx)/dr
print("Numero de anillos:", nr)

nr = 1

for j in range(nr):
    for i in range(p):
        
        x1, y1 = vertices[i]
        if i == p-1:
            x2, y2 = vertices[0]
        else:
            x2, y2 = vertices[i+1]

        if i == p-1:
            x3, y3 = vertices[1]
        elif i == p-2:
            x3, y3 = vertices[0]
        else:
            x3, y3 = vertices[i+2]
        vector1x = x2 - x1
        vector1y = y2 - y1
        vector2x = x3 - x2
        vector2y = y3 - y2
        angleY = angle_between_vectors(vector1x, vector1y, vector2x, vector2y)

        angleY= angleY*math.pi/180
        print("angleY:", angleY)

        if i == 0 and j == 0:    
            if angleY%90 != 0:
                di = distancia(x1, y1, x2, y2)-(LX/(math.tan(angleY)))      
            else:
                di = distancia(x1, y1, x2, y2)
        else:
                di = distancia(x1, y1, x2, y2)

        print("di:", di)             

        # Numero de waypoints
        nw = int(round((di-Ovy)/dw))

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0:
            catetox = 0
            catetoy = dw
        else:
            angulo = math.atan(dy/dx) 
            print("angulo"+str(angulo))   
            catetox = math.cos(angulo)*dw
            catetoy = math.sin(angulo)*dw

        for k in range(nw):
            if k == 0:
                if i == 0 and j == 0:   
                    if dx == 0:
                        catetoxO = 0
                        catetoyO = dw
                    else:  
                        catetoxO = math.cos(angulo)*(LX/math.tan(angleY))
                        catetoyO = math.sin(angulo)*(LX/math.tan(angleY))
                    print((LX/2),(LY/2))
                    wp_dron.append(((x1-catetoxO)+(LX/2),(y1-catetoyO)+(LY/2)))
                    print("PointOrigen"+str( wp_dron[k]))

                else:    
                    wp_dron.append((x1+(LY/2),y1+LX/2))
            else:
                xwp , ywp = wp_dron[k-1]
                wp_dron.append((xwp+catetox,ywp+catetoy))
                di = distancia(x1, y1, x2, y2)-(LX/(math.tan(angleY)))
            
            print("Point"+str( wp_dron[k]))



                
                




        # Ovy recalculado
        Ovy = (nw*LY-di)/(nw-1)
        # dw recalculado
        dw = (di-LY)/(nw-1)

        




        




