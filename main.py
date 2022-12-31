"""
    Título del proyecto: RECONOCIMIENTO DE IMÁGENES
    Descripción del proyecto: Reconocimiento de 3 regiones e una imágen digital.
    Autor: Cristian Del Angel Fiscal
    Fecha: 25/12/2022
    Licencia: Ninguna

    Librerías:
    tkinter: Kit de herramientas GUI.
    bayesiano_param: Implementación del algoritmo distancia euclidiana
    knn_dis_min: Implementación del algoritmo K-NN con distancia mínima
    perceptron: Implementación del algoritmo perceptrón multicapa
"""

from tkinter import *
from tkinter import ttk

from bayesiano_param import DistanciaEuclidiana
from knn_dis_min import KNNDisMin
from perceptron import PerceptronMulticapa

class Aplicacion():
    """
        Interfaz Gráfica de Usuario que permite elegir al usuario uno de los
        3 métodos de clasificación.
    """

    def __init__(self, r) -> None:
        """
            Constructor de la clase.

            Parámetros:
            r: Widget principal de la GUI
        """

        r.title('Reconocimiento de imágenes')
        r.geometry('400x100')
        barra_menu = Menu(r)
        r.config(menu=barra_menu)

        #------------- ELEMENTOS DE LA BARRA -------------
        bayesiano = Menu(barra_menu, tearoff=0)
        r_neuronal = Menu(barra_menu, tearoff=0)

        #------------- ASIGNACIÓN ELEMENTOS DE LA BARRA -------------
        barra_menu.add_cascade(label='Enfoque Bayesiano', menu=bayesiano)
        barra_menu.add_cascade(label='Enfoque Neuronal', menu=r_neuronal)

        bayesiano.add_command(label='Distancia Euclidiana', command=self.algoritmo_BP)
        bayesiano.add_command(label='K-NN', command=self.algoritmo_knn)

        r_neuronal.add_command(label='Perceptrón Multicapa', command=self.algoritmo_PMC)

        #------------- FRM PINCIPAL -------------
        frm_principal = ttk.Frame(r)
        frm_principal.pack()

        l_instrucciones = ttk.Label(frm_principal, text='Por favor, seleccione un algoritmo para comenzar.')
        l_instrucciones.grid(row=0, column=0, columnspan=3)

        btn_euclidiano = ttk.Button(frm_principal, text='Distancia euclidiana', command=self.algoritmo_BP)
        btn_euclidiano.grid(row=1, column=0)
        btn_red_neuronal = ttk.Button(frm_principal, text='K-NN', command=self.algoritmo_knn)
        btn_red_neuronal.grid(row=1, column=1)
        btn_asociacion = ttk.Button(frm_principal, text='Perceptrón Multicapa', command=self.algoritmo_PMC)
        btn_asociacion.grid(row=1, column=2)

        # Los elementos del frame se configuran para tener separación
        for child in frm_principal.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def algoritmo_BP(self) -> None:
        """
            Llamada a la GUI del algoritmo de distancia euclidiana.
        """

        DistanciaEuclidiana()

    def algoritmo_knn(self) -> None:
        """
            Llamada a la GUI del algoritmo K-NN con distancia mínima.
        """

        KNNDisMin()

    def algoritmo_PMC(self) -> None:
        """
            Llamada a la GUI del algoritmo perceptrón multicapa.
        """

        PerceptronMulticapa()

#-----------------MAIN--------------
raiz = Tk()
Aplicacion(raiz)
raiz.mainloop()