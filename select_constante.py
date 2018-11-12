from ANS import *

# Guarda la posición en la que se encuentra cada 1
def calcularSelectConstante(archivo, comparar="1"):
    with open(archivo,'rb') as file:

        flag = 0    # permite leer el overhead
        S = {}
        # Para cada linea en el archivo
        for line in file:
            # Si flag es 0, entonces se va a leer el tamaño de página
            if flag == 0:
                # Se convierte la línea actual a un arreglo de bytes
                actual = bytearray(line)
                # Como el último byte es el separador, entonces se convierte
                # a entero los primeros bytes de la línea sin el último elemento
                M = int.from_bytes(bytes(actual[:-1]), byteorder=endian)
                flag += 1

            # Si flag es 1, entonces se van a leer las proporciones
            elif flag == 1:
                # La línea actual se convierte a un arreglo de bytes
                actual = bytearray(line)
                # La letra corresponde al primer byte
                letra = actual[0]
                # Si es 0, ya terminamos de leer el overhead
                if letra == 0:
                    flag += 1
                else:
                    # Sino, lee los siguientes bytes y los transforma a entero
                    frecuencia = int.from_bytes(bytes(actual[1:-1]),byteorder=endian)
                    letra = chr(letra)
                    # Guarda la relación de cada letra con su frecuencia
                    S[letra] = frecuencia
            else:
                # Al final se calcula el estado final leyendo la última línea del archivo
                estado = int.from_bytes(bytearray(line),byteorder=endian)

    # Esta es la cadena que contiene el texto reconstruido
    arr = []
    contador = 0
    # Calcula el estado inicial de cada letra
    ro = calcularRo(S)
    # Mientras el estado exista y no sea el 0, entonces...
    while estado is not None and estado != 0:
        # Se calcula el estado anterior y la letra
        estado, letra = previousState(estado, S, M, ro)
        if letra == comparar:
            arr.insert(0,contador)
        contador += 1

    newarr = [0]+[contador - elemento for elemento in arr]

    return newarr,contador

# Dada la cantidad de 1's encontrar la posición en el texto
# donde aparece la primer ocurrencia de los i 1's
def selectConstante(arr,i):
    return arr[i]

def rankBinario(arr,i):

    if i < selectConstante(arr,1):
        return 0

    if i > selectConstante(arr,len(arr)-1):
        return len(arr)-1

    p = 0
    r = len(arr)

    while r-p > 1:
        # Mitad del arreglo
        m = (p+r)//2

        # Posicion en la que se encuentra el m-simo 1
        elemento = selectConstante(arr,m)

        # Si la posicion del m-esimo 1 es la misma que se busca
        if elemento == i:
            # Regresa el indice m, que es igual a la cantidad de 1's hasta la posicion de elemento
            return m

        if m > 0:
            comparar = selectConstante(arr,m-1)
            if elemento > i and i > comparar:
                return m-1

        if i<elemento:
            r = m
        else:
            p = m

    return -1

def access(arr,i):
    if i == 0:
        return rankBinario(arr,i)

    return rankBinario(arr,i) - rankBinario(arr,i-1)
