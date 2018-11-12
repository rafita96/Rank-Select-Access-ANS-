from ANS import *

# Guarda la cantidad de 1's que hay hasta cada posición
def calcularRankConstante(archivo, comparar="1"):
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
    arr = [0]
    contador = 0
    # Calcula el estado inicial de cada letra
    ro = calcularRo(S)
    # Mientras el estado exista y no sea el 0, entonces...
    while estado is not None and estado != 0:
        # Se calcula el estado anterior y la letra
        estado, letra = previousState(estado, S, M, ro)
        if letra == comparar:
            arr.insert(0,arr[0]+1)
        else:
            arr.insert(0,arr[0])
        contador += 1


    newarr = [arr[0] - elemento for elemento in arr]

    return newarr,contador


# Utiliza el rankConstante para encontrar la posición en el texto
# donde aparece la primer ocurrencia de los i 1's
def selectBinario(arr,i):

    p = 0
    r = len(arr)

    while r-p > 1:
        m = (p+r)//2
        elemento = rankConstante(arr,m)
        if elemento == i:
            
            if m == 0:
                return m

            anterior = arr[m-1]
            while anterior == i:
                m -= 1
                anterior = arr[m-1]

            return m

        if i < elemento:
            r = m
        else:
            p = m

    return -1

# Dada la posición i en el texto, se regresa la
# cantidad de 1's que hay en el subarreglo arr[0...i]
def rankConstante(arr,i):
    if i < len(arr):
        return arr[i]
    return -1
    
def access(arr,i):
    if i == 0:
        return rankConstante(arr,i)

    return rankConstante(arr,i) - rankConstante(arr,i-1)
