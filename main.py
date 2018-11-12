import math, os

endian = 'little'

# Calcula los bytes necesarios para representar un entero en bits
def bytes_needed(n):
    if n == 0:
        return 1

    return int(math.log(n, 256)) + 1


# Calcula el siguiente estado, dado el estado actual,
# la letra de entrada, las proporciones para cada letra,
# el tamaño de página y el estado inicial para cada letra.
def nextStateBy(estado, entrada, S, M, ro):
    q = estado//S[entrada]
    r = estado % S[entrada]

    res = q*M + r + ro[entrada]
    return res

# Calcula el estado anterior y la letra con la que proviene, dado
# el estado actual, las proporciones para cada letra, el tamaño de página
# y el estado inicial para cada letra.
def previousState(estado,S,M,ro):
    for letra in S.keys():
        r = 1 + (estado -1)%M
        j = (estado-r)//M
        s = j*(S[letra]) - ro[letra] + r
        probable = nextStateBy(s,letra,S,M,ro)
        if probable == estado:
            return (s,letra)

    return (None,None)

# Calcula el estado inicial para cada letra.
def calcularRo(S):
    letras = sorted(list(S.keys()))
    ro = {letras[0]: 1}

    for i in range(1,len(letras)):
        letra = letras[i]
        ro[letra] = ro[letras[i-1]] + S[letras[i-1]]

    return ro

# Calcula la proporción de cada letra con respecto a todas
# las letras en el texto
def calcularFrecuencias(texto):

    conteo = {}
    n = len(texto)
    # Si el texto está vacío no hace algo
    if n == 0:
        return {}

    # Primero se cuentan las ocurrencias de cada letra
    for letra in texto:
        if letra in conteo.keys():
            conteo[letra] += 1
        else:
            conteo[letra] = 1

    frecuencias = {}
    mcd = float('inf')
    # Se busca la ocurrencia más pequeña para normalizar
    # con respecto a ella
    for letra in conteo.keys():
        if conteo[letra] < mcd:
            mcd = conteo[letra]

    M = 0   # acumula el tamaño de página
    for letra in conteo.keys():
        # Se normaliza la frecuencia de cada letra
        # con respecto a la frecuencia más pequeña
        res = (conteo[letra]-1)//mcd + 1
        frecuencias[letra] = res
        M += res

    return M,frecuencias

# Obtiene el caracter para el espaciado
def getEspaciado():
    return '\n'.encode('utf-8')

# Calcula los bits necesarios para poder decodificar
def encodeOverhead(M,S):
    overhead = []
    espaciado = getEspaciado()

    needed = bytes_needed(M)    # Bytes necesarios para guardar el tamaño de página
    MCoded = (M).to_bytes(needed, byteorder=endian)

    overhead.append(MCoded)
    overhead.append(espaciado)

    # Se convierte a bytes la tabla de frecuencias
    for letra in S.keys():
        letraCoded = letra.encode('utf-8')  # La letra pesa exactamente un byte
        overhead.append(letraCoded) 

        # Se calculan los bytes necesarios para cada frecuencia
        needed = bytes_needed(S[letra])
        frecCoded = (S[letra]).to_bytes(needed, byteorder=endian) # Se codifica la frecuencia
        overhead.append(frecCoded)
        overhead.append(espaciado) # Al final se pone un separador para no confundir

    # Se codifica un 0 como final del overhead
    overhead.append((0).to_bytes(1,byteorder=endian))
    overhead.append(espaciado)
    return overhead


# Codifica un archivo
def encode(archivo):
    with open(archivo) as file:
        texto = file.read()

    # Se consiguen las frecuencias y el tamaño de página
    M,S = calcularFrecuencias(texto)

    # Se calcula el estado inicial
    ro = calcularRo(S)
    estado = 0  # Contiene el estado actual

    # Para cada letra en el texto se calcula el estado correspondiente
    for letra in texto:
        estado = nextStateBy(estado, letra, S, M,ro)

    # Se calcula el overhead
    overhead = encodeOverhead(M,S)

    index = archivo.find('.')
    archivoCodificado = archivo[:index]+'.coded'
    # Se guarda en un archivo el texto codificado
    # y en bytes para reducir el espacio
    with open(archivoCodificado, "wb") as file:
        for bit in overhead:
            file.write(bit)

        # Se calculan los bytes necesarios para el estado
        needed = bytes_needed(estado)
        file.write((estado).to_bytes(needed, byteorder=endian))

    # Compara los pesos de los archivos
    peso_1 = os.path.getsize(archivo)
    peso_2 = os.path.getsize(archivoCodificado)
    print(archivoCodificado,'creado.')
    if peso_1 >= peso_2 and peso_2 != 0:
        print(100 - (peso_2*100)/peso_1,'% de compresion')
    else:
        print('Pesa más.')

# Decodifica un archivo
def decode(archivo):
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
    reconstruccion = ""
    # Calcula el estado inicial de cada letra
    ro = calcularRo(S)
    # Mientras el estado exista y no sea el 0, entonces...
    while estado is not None and estado != 0:
        # Se calcula el estado anterior y la letra
        estado, letra = previousState(estado, S, M, ro)
        # Se reconstruye el texto
        reconstruccion = letra+reconstruccion

    # Guarda el texto reconstruido en un archivo
    index = archivo.find('.')
    archivoDeCodificado = archivo[:index]+'.decoded' 
    with open(archivoDeCodificado, 'w+') as file:
        file.write(reconstruccion)

    print(archivoDeCodificado,'creado.')

def main():

	archivo = 'texto.txt'
	encode(archivo)

    # x = input("Codificar (1) o Decodificar (2): ")
    # if int(x) == 1:
    #     archivo = input('Nombre del archivo a codificar: ')
    #     encode(archivo)
    # elif int(x) == 2:
    #     archivo = input('Nombre del archivo a decodificar: ')
    #     decode(archivo)

main()