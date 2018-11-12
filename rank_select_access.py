from BinaryOperator import *

def main():

    archivo = 'texto.coded'
    # Crea el operador binario con rank constante para 1's
    b1,contador = rankConstante(archivo)
    # Crea el operador binario con select constante para 1's
    b2,contador = selectConstante(archivo)

    print("Rank y Select para 1")
    print("rank:",b1.arr)
    print("select:", [ b1.select(i) for i in range(len(b1.arr)) if b1.select(i) != -1 ])
    print()
    print("select:",b2.arr)
    print("rank:", [b2.rank(i) for i in range(contador+1)])
    print()

    # Cadena original
    cadena = ""
    for i in range(contador):
        cadena += str(b1.access(i+1))

    print(cadena)

    print("Rank y Select para 0")
    # Crea el operador binario con rank constante para 0's
    b1,contador = rankConstante(archivo, "0")
    # Crea el operador binario con select constante para 0's
    b2,contador = selectConstante(archivo, "0")
    print("rank:",b1.arr)
    print("select:", [ b1.select(i) for i in range(len(b1.arr)) if b1.select(i) != -1 ])
    print()
    print("select:",b2.arr)
    print("rank:", [b2.rank(i) for i in range(contador+1)])


main()
