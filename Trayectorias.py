import math

vertices = [(-6.68,5.5), (1,3.72), (1.66,-2.22), (-8.54,-1.42), (-10.56,2.44)]
# Campo de vision
LX = 1
LY = 1
# Sobrelapamiento minimo en X y Y
Ovx = 0.1
Ovy = 0.1
# Distancia entre anillos
dr = LX-Ovx
# Distancia entre weypoints
dw = LY-Ovy

p = len(vertices)
sum_x = sum([v[0] for v in vertices])
sum_y = sum([v[1] for v in vertices])
centroid_x = sum_x / p
centroid_y = sum_y / p

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def angle_between_vectors(x1, y1, x2, y2):
    dot_product = x1 * x2 + y1 * y2
    mag_product = math.sqrt(x1**2 + y1**2) * math.sqrt(x2**2 + y2**2)
    return math.degrees(math.acos(dot_product/mag_product))

print("Centroid: "+str(centroid_x)+","+str(centroid_y))

dcp = float("inf")
for i in range(p):

    x1, y1 = vertices[i]
    x2, y2 = vertices[(i + 1) % p]
    dx = x2 - x1
    dy = y2 - y1
    distance = abs(dx * (centroid_y - y1) - dy * (centroid_x - x1)) / math.sqrt(dx**2 + dy**2)

    if distance < dcp:
        dcp = distance

print("La apotema del poligono es:", dcp)

# Numero de anillos
nr = (dcp-Ovx)/dr
print("Numero de anillos:", nr)

for j in range(nr):
    for i in range(p):
        x1, y1 = vertices[i]
        if i == p-1:
            x2, y2 = vertices[0]
        else:
            x2, y2 = vertices[i+1]
        di = distance(x1, y1, x2, y2)

        print("di:", di)

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
        print("angleY:", angleY)

        # Numero de waypoints
        nw = (di-Ovy)/dw
        




