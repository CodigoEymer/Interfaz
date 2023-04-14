import math

# Definir las coordenadas del punto a rotar
x = 0
y = 6

# Definir las coordenadas del centroide
x0 = 3
y0 = 4

# Definir el angulo de rotacion en grados
theta = -30

# Convertir el angulo de grados a radianes
theta = math.radians(theta)

# Calcular las coordenadas del punto rotado
x_rotated = (x - x0) * math.cos(theta) - (y - y0) * math.sin(theta) + x0
y_rotated = (x - x0) * math.sin(theta) + (y - y0) * math.cos(theta) + y0

# Mostrar las coordenadas del punto original y del punto rotado
print("Punto original: ({}, {})".format(x, y))
print("Punto rotado: ({}, {})".format(x_rotated, y_rotated))
