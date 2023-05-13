
import math

def calcular_distancia_total(V):
    distancia_total = 0

    for i in range(1, len(V)):
        punto_actual = V[i]
        punto_anterior = V[i-1]
        distancia = math.sqrt((punto_actual[0] - punto_anterior[0])**2 + (punto_actual[1] - punto_anterior[1])**2)
        distancia_total += distancia

    return distancia_total

V = [(1,3),(2,2),(4,2),(4,3),(2,3),(2,4),(4,4)]
print(calcular_distancia_total(V))
