from PyQt5.QtWidgets import QApplication, QFileDialog
import sys

def leer_datos(archivo):
    with open(archivo, 'r') as file:
        lines = file.readlines()

    datos = {}
    clave_actual = None
    for line in lines:
        line = line.strip()
        if line in ['coords', 'area', 'wp_recarga']:
            clave_actual = line
            datos[clave_actual] = []
        elif clave_actual:
            valor = eval(line)
            if clave_actual == 'area':
                datos[clave_actual] = valor[0]
            else:
                datos[clave_actual].append(valor)

    return datos

def seleccionar_archivo():
    app = QApplication(sys.argv)
    archivo = QFileDialog.getOpenFileName(
        None, 
        "Selecciona un archivo de texto", 
        "", 
        "Archivos de texto (*.txt)"
    )[0]
    app.quit()
    return archivo

def main():
    archivo = seleccionar_archivo()
    if not archivo:
        print("No se seleccionó ningún archivo.")
        return

    datos_leidos = leer_datos(archivo)

    coords = datos_leidos.get('coords', [])
    area = datos_leidos.get('area', 0)
    wp_recarga = datos_leidos.get('wp_recarga', [])

    print("coords: ", coords)
    print("area: ", area)
    print("wp_recarga: ", wp_recarga)

if __name__ == "__main__":
    main()
