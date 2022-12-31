"""
    Título del proyecto: MÓDULO PARA OPERAR ARCHIVO CSV
    Descripción del proyecto: Funciones necesarias para escribir, modificar o leer archivo csv.
    Autor: Cristian Del Angel Fiscal
    Fecha: 19/12/2022
    Licencia: Ninguna

    Librerías:
    csv: Escribir y leer datos tabulares
    pickle: Para transformar un objeto complejo en una secuencia de bytes
"""

import csv
import pickle

class ArchivoCSV():
    """
        Implementa funciones para operar archivos csv; escribir, leer,
        eliminar, modificar registros de tipo de dato diccionario.
    """

    def escribir_datos(self, lista_diccs) -> None:
        """
            Escribe el archivo y agrega los patrones de la primer clase.

            Parámetros:
            lista_diccs: 
             Lista de diccionarios de datos donde se tiene la información de los patrones; 
             No. caso, canal R, canal G, canal B, clase asignada
        """

        with open("datos.csv", "w") as archivo:
            nombre_campos = ['CASO', 'R', 'G', 'B', 'CLASE']

            escritor = csv.DictWriter(archivo, fieldnames=nombre_campos)
            escritor.writeheader()
            escritor.writerows(lista_diccs)

            archivo.close()

    def agregar_datos(self, lista_diccs) -> None:
        """
            Agrega los patrones de la siguiente clase

            Parámetros:
            lista_diccs: 
             Lista de diccionarios de datos donde se tiene la información de los patrones;
             No. caso, canal R, canal G, canal B, clase asignada
        """

        with open("datos.csv", "a") as archivo:
            nombre_campos = ['CASO', 'R', 'G', 'B', 'CLASE']

            escritor = csv.DictWriter(archivo, fieldnames=nombre_campos)
            escritor.writerows(lista_diccs)

            archivo.close()

    def escribir_dato(self, fila) -> None:
        """
            Después de analizar el patrón desconocido y asignarle un número de CASO 
            y su CLASE, se agrega la nueva fila en el archivo csv.

            Parámetros:
             fila: Diccionario de datos donde se tiene la información de un patrón;
             No. caso, canal R, canal G, canal B, clase asignada
        """

        with open("datos.csv", "a") as archivo:
            nombre_campos = ['CASO', 'R', 'G', 'B', 'CLASE']
            escritor = csv.DictWriter(archivo, fieldnames=nombre_campos)
            escritor.writerow(fila)

            archivo.close()

    def leer_datos(self) -> list:
        """
            Devueleve todos los elementos del archivo csv.

            Retorno:
            Lista de diccionarios de los patrones de aprendizaje.
        """

        with open("datos.csv", 'r') as archivo:
            lector = list(csv.DictReader(archivo))

            archivo.close()

            return lector

    def eliminar_dato(self) -> None:
        """
            Elimina la última fila del archivo csv y llama a la función
            que actualiza ese cambio en el archivo.
        """

        with open("datos.csv", "r") as lectura:
            lineas = list(csv.DictReader(lectura))
            lineas.pop()

            lectura.close()

        self.escribir_nuevo(lineas)

    def escribir_nuevo(self, dic) -> None:
        """
            Sobreescribe el archivo después de eliminar la última fila.

            Parámetros:
            dic: Lista de diccionarios de todos los casos de aprendizaje
        """

        with open("datos.csv", "w") as archivo:
            nombre_campos = ['CASO', 'R', 'G', 'B', 'CLASE']

            escritor = csv.DictWriter(archivo, fieldnames=nombre_campos)
            escritor.writeheader()
            escritor.writerows(dic)

            archivo.close()

    def lista_a_diccionario(self, lista, clase) -> list:
        """
            Crea un diccionario por cada patrón que lee de la lista, además
            le asigna la clase a la que pertenece según el parámetro dado por
            el usuario.

            Parámetros:
            lista: Lista de patrones numpy correspondientes a los componentes RGB de una región
            clase: Entero que hace referencia a la clase que pertenece

            Retorno:
            Lista de diccionarios
        """

        # Solo se usa cuando ya haya datos en el archivo csv
        datos = self.leer_datos()
        contador_caso = int(datos[-1]['CASO'])

        lista_salida = []

        # Se usa cuando no hay datos en el archivo csv
        #contador_caso = 0

        for patron in lista:
            contador_caso += 1

            p_dicc = {'CASO':contador_caso, 'R':patron[0], 'G':patron[1], 'B':patron[2], 'CLASE':clase}

            lista_salida.append(p_dicc)

        return lista_salida

if __name__ == '__main__':
    controlador = ArchivoCSV()

    # Leer lista de archivo binario
    fichero = open("BinarioregTierra", "rb")
    # Para obtener la información binaria e interpretarla
    lista_recuperada = pickle.load(fichero)
    fichero.close()

    # Se toma únicamente el 70 por ciento de datos de cada región
    calcular_70 = int(len(lista_recuperada) * 0.7)
    ptrs_elegidos = lista_recuperada[:calcular_70]

    print(len(lista_recuperada))
    print(len(ptrs_elegidos))

    # Sólo se usa cuando no haya datos en el archivo csv
    #lista_diccs = controlador.lista_a_diccionario(ptrs_elegidos)

    lista_diccs = controlador.lista_a_diccionario(ptrs_elegidos, 3)

    controlador.agregar_datos(lista_diccs)

    # Sólo se usa cuando no haya datos en el archivo csv
    #controlador.escribir_datos(lista_diccs)