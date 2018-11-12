# Asymetrical Numerical System

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