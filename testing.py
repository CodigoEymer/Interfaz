
import math

def angle_between_vectors(x1, y1, x2, y2):
    print(x1,y1,x2,y2)
    dot_product = x1 * x2 + y1 * y2
    print(dot_product)
    mag_product = math.sqrt(x1**2 + y1**2) * math.sqrt(x2**2 + y2**2)
    print(mag_product)
    print(y2)
    if y2<0:
        theta= -(math.acos(dot_product/mag_product))
    else:
        theta= (math.acos(dot_product/mag_product))
    return theta
    
if __name__ == "__main__":    
    vertices=[(5,3),(7,5),(2,3)]
    x0, y0 = vertices[-1]
    print(x0,y0)
    x1, y1 = vertices[0]
    print(x1,y1)
    x2, y2 = vertices[1]
    print(x2,y2)
    
    vector1x = float(x0 - x1)
    vector1y = float(y0 - y1)
    vector2x = float(x2 - x1)
    vector2y = float(y2 - y1)
    
    angleY = angle_between_vectors(vector1x, vector1y, vector2x, vector2y)
    
    print(angleY*(180/math.pi))
