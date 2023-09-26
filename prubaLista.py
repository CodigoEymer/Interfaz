class Main:
    def __init__(self):
        lista = []
        colores =[]
        colora = "/"
        colorb = "-"

        colores.append(colora)
        colores.append(colorb)

        
        crecer(colores,lista)


def crecer(colores, lista):
    for i in range(len(colores)):
        lista.append([str(colores[i]),(0.15,0,12)])
    print(str(lista))

if __name__ == "__main__":
    main = Main()

