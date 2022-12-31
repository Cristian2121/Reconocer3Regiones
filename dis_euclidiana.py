"""
    Título del proyecto: ALGORITMO DISTANCIA EUCLIDIANA
    Descripción del proyecto: Basado en dos vectores, cálcula su distancia respectiva.
    Autor: Cristian Del Angel Fiscal
    Fecha: 13/11/2022
    Licencia: Ninguna

    Librerías:
    numpy: Convertir tuplas en vectores numpy para facilitar la operación de vectores
"""

import numpy as np

def distancia_euclidiana(vector, patron) -> float:
    """
        Convierte las dos tuplas recibidas en vectores numpy, 
        resta sus elementos, uno a uno, y los eleva al cuadrado, 
        luego suma todos los elementos resultantes y al finalizar 
        aplica raíz cuadrada.

        Parámetros:
        vector: Tupla que representa los centroides de una región
        patron: Tupla que representa los componentes RGB de la imágen

        Retorno:
        Un valor flotante no negativo
    """

    pat = np.array(patron)
    vec = np.array(vector)

    resta_cuadrada = np.square(vec - pat)
    suma = np.sum(resta_cuadrada)
    dis = np.sqrt(suma)

    return dis

if __name__ == '__main__':
    patron = np.array( (183, 125, 44) )

    d_c1 = distancia_euclidiana(patron, (206.6, 168.8, 131))
    d_c2 = distancia_euclidiana(patron, (89, 130.6, 59))
    d_c3 = distancia_euclidiana(patron, (24.8, 44.4, 179.8))

    if d_c1 > d_c2 > d_c3 or d_c2 > d_c1 > d_c3:
        print("El patrón pertenece a la clase C3")
    elif d_c1 > d_c3 > d_c2 or d_c3 > d_c1 > d_c2:
        print("El patrón pertenece a la clase C2")
    elif d_c3 > d_c2 > d_c1 or d_c2 > d_c3 > d_c1:
        print("El patrón pertenece a la clase C1")