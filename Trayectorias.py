import math
#input
vertices = [(-1,-2),(1,-2),(3,0),(1,1),(-1,1),(-3,0)]
#output
wp_dron =[]
# Campo de vision
LX = 1.0
LY = 1.0
# Sobrelapamiento minimo en Y
Ovx = 0.1


# Distancia entre vertices
di = 0

p = len(vertices)
sum_x = sum([v[0] for v in vertices])
sum_y = sum([v[1] for v in vertices])
centroid_x = sum_x / p
centroid_y = sum_y / p

cp=(centroid_x,centroid_y)

def distancia(x1, y1, x2, y2):
    r= math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return r

def angle_between_vectors(x1, y1, x2, y2):
    dot_product = x1 * x2 + y1 * y2
    mag_product = math.sqrt(x1**2 + y1**2) * math.sqrt(x2**2 + y2**2)

    if y2<0:
        tetha= -(math.acos(dot_product/mag_product))
    else:
        tetha= (math.acos(dot_product/mag_product))
    return (tetha)

dcp = float("inf")

for m in range(p): 
    x1, y1 = vertices[m]
    x2, y2 = vertices[(m + 1) % p]
    dx = x2 - x1
    dy = y2 - y1
    distance = abs(dx * (centroid_y - y1) - dy * (centroid_x - x1)) / math.sqrt(dx**2 + dy**2)
    if distance < dcp:
        dcp = distance

# Distancia entre anillos
dr = LX-Ovx

# Numero de anillos
nr = (dcp-Ovx)/dr
num_rings = int(math.ceil(nr))
num_rings=1

#Ovx recalculado
#Ovx=(num_rings*LX-dcp)/(num_rings-1)
#dr recalculado
#dr=(dcp-LX)/(num_rings-1)

for j in range(num_rings):
    for i in range(p):
        
        x0, y0 = vertices[i-1]
        
        if i == p-1:
            x1, y1 = vertices[-1]
        else:
            x1, y1 = vertices[i]

        if i == p-1:
            x2, y2 = vertices[0]
        elif i == p-2:
            x2, y2 = vertices[-1]
        else:
            x2, y2 = vertices[i+1]
        vector1x = float(x0 - x1)
        vector1y = float(y0 - y1)
        vector2x = float(x2 - x1)
        vector2y = float(y2 - y1)
        angleY = angle_between_vectors(vector1x, vector1y, vector2x, vector2y)
        print("angle interior: ", str(angleY*180/(math.pi)))
        
        if i == 0 and j == 0:    
            di = distancia(x1, y1, x2, y2)-(LX/(math.tan(angleY)))      
        else:
            di = distancia(x1, y1, x2, y2)

        # Sobrelapamiento minimo en Y
        Ovy = 0.1

        # Distancia entre weypoints
        dw = LY-Ovy

        # Numero de waypoints
        nw = (di-Ovy)/dw
        num_wp_line = int(math.ceil(nw))

        if nw==1:
            Ovy = 0.0
        else:
            # Ovy recalculado
            #print(nw,LY,di,nw)    
            Ovy = (num_wp_line*LY-di)/(num_wp_line-1)
            #print("Ovy: ", str(Ovy))
            # dw recalculado
            dw = (di-LY)/(num_wp_line-1)
            #print("dw: ", str(dw))

        dx = float(x2 - x1)
        dy = float(y2 - y1)
        
        angulo = angle_between_vectors(1.0, 0.0, dx, dy)
        catetox = math.cos(angulo)*dw
        catetoy = math.sin(angulo)*dw

        for k in range(num_wp_line):
            if k == 0:
                h=   math.sqrt((LX/2)**2 + (LY/2)**2)
                angulo_phi=math.atan(LX/LY)
                #print("angle phi: ", str(angulo_phi*180/(math.pi)))
                angulo_alpha = angulo_phi+angulo
                #print("angulo: ", str(angulo*180/(math.pi)))
                if i == 0 and j == 0:   
                    if dx == 0:
                        catetoxO = 0
                        catetoyO = dw
                    else:  
                        catetoxO = math.cos(angulo)*(LX/math.tan(angleY))
                        catetoyO = math.sin(angulo)*(LX/math.tan(angleY))
                    wp_dron.append(((x1+catetoxO)+h*math.cos(angulo_alpha),(y1+catetoyO)+h*math.sin(angulo_alpha)))

                else:
                    wp_dron.append((x1+h*math.cos(angulo_alpha),y1+h*math.sin(angulo_alpha)))
            else:
                indice=  (len(wp_dron))-1
                xwp , ywp = wp_dron[indice]
                wp_dron.append((xwp+catetox,ywp+catetoy))

            print(str(wp_dron[(len(wp_dron))-1]))
        

        
        

 