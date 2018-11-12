import rank_constante, select_constante

# Clase que permite homogeneizar las operaciones rank, select y access.
class BinaryOperator:

    def __init__(self, arr, rank, select, access):
        self.arr = arr 
        self.rank_p = rank 
        self.select_p = select
        self.access_p = access

    # Depende como se defina el arreglo constante (si es para 0 o 1).
    # Si está definido para 1, dada una posición en el texto 
    # regresa la cantidad de 1's que hay en el texto hasta esa posición
    def rank(self, i):
        return self.rank_p(self.arr,i)

    # Depende como se defina el arreglo constante (si es para 0 o 1).
    # Si está definido para 1, busca la posición del i-ésimo 1.
    def select(self,i):

        return self.select_p(self.arr,i)

    # Dada la posición regresa un 0 o un 1, dependiendo el número que 
    # se encuentre en esa posición.
    def access(self,i):
        return self.access_p(self.arr, i)

# Define las operaciones binarias select, rank y access con el arreglo rank constante.
# @param    comparar    "1" si se quiere calcular para los 1's o "0" si 
#                       se quiere calcular para los 0's.
def rankConstante(archivo, comparar="1"):
    arr,contador = rank_constante.calcularRankConstante(archivo, comparar)
    rank = rank_constante.rankConstante
    select = rank_constante.selectBinario
    access = rank_constante.access

    b = BinaryOperator(arr,rank,select, access)

    return b,contador

# Define las operaciones binarias select, rank y access con el arreglo select constante
# @param    comparar    "1" si se quiere calcular para los 1's o "0" si 
#                       se quiere calcular para los 0's.
def selectConstante(archivo,comparar="1"):
    arr,contador = select_constante.calcularSelectConstante(archivo, comparar)
    rank = select_constante.rankBinario
    select = select_constante.selectConstante
    access = select_constante.access

    b = BinaryOperator(arr,rank,select, access)
    return b,contador