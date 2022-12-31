"""
    Título del proyecto: GUI DISTANCIA EUCLIDIANA
    Descripción del proyecto: Permite seleccionar una imágen, y clasificarla según el método distancia euclidiana.
    Autor: Cristian Del Angel Fiscal
    Fecha: 23/11/2022
    Licencia: Ninguna

    Librerías:
    tkinter: Kit de herramientas GUI.
    cv2: Abrir imágen y extraer RGB de pixel seleccionado
    numpy: Convertir valores RGB en vector numpy para fácil operación de vectores
    dis_euclidiana: Implementación del algoritmo de distancia euclidiana
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox

import cv2
import numpy as np

from dis_euclidiana import distancia_euclidiana

class DistanciaEuclidiana():
    """
        Interfaz Gráfica de Usuario que permite seleccionar una imágen para extraer
        los componentes RGB de un pixel, para posteriormente procesarlo con la técnica
        de clasificación de distancia euclidiana, y enviar una respuesta al usuario final.
    """

    def __init__(self) -> None:
        """
            Constructor de la clase.
        """

        nueva_ventana = Tk()
        nueva_ventana.title('Distancia Euclidiana')

        #------------- VARIABLES GLOBALES -------------
        self.dir_img = StringVar()

        frm_principal = ttk.Frame(nueva_ventana)
        frm_principal.pack()

        l_titulo = ttk.Label(
            frm_principal, 
            text="""
                Análisis con el método Bayesiano paramétrico: \n
                Para una distribución normal o distancia Euclidiana (dE)
            """
        )
        l_titulo.grid(row=0, column=0, columnspan=2)

        l_red = ttk.Label(frm_principal, text="R:")
        l_red.grid(row=1, column=0)
        l_green = ttk.Label(frm_principal, text="G:")
        l_green.grid(row=2, column=0)
        l_blue = ttk.Label(frm_principal, text="B:")
        l_blue.grid(row=3, column=0)

        self.e_red = ttk.Entry(frm_principal, justify='center')
        self.e_red.grid(row=1, column=1)
        self.e_green = ttk.Entry(frm_principal, justify='center')
        self.e_green.grid(row=2, column=1)
        self.e_blue = ttk.Entry(frm_principal, justify='center')
        self.e_blue.grid(row=3, column=1)

        #------------- BOTONES -------------
        btn_euc_manual = ttk.Button(frm_principal, text='Patrón digitado', command=self.evento_manual)
        btn_euc_manual.grid(row=5, column=0)

        btn_euclidiano = ttk.Button(frm_principal, text='Desde imagen', command=self.abrir_imagen)
        btn_euclidiano.grid(row=5, column=1)

        for child in frm_principal.winfo_children():
            child.grid_configure(padx=5, pady=5)

        nueva_ventana.mainloop()

    def abrir_imagen(self) -> None:
        """
            Permite  elegir una imágen del explorador de archivos del usuario,
            y luego almacena la ruta relativa en una variable de la clase para
            su posterior uso en otro método.
        """

        try:
            archivo = filedialog.askopenfilename(
                title="Seleccionar imagen", 
                filetypes=(("PNG", "*.png"), ("JPG", "*.jpg"), ("JPEG", "*.jpeg"))
            )

            self.dir_img = archivo

            self.trabajar_imagen()
        except:
            messagebox.showerror('Error', 'No se seleccionó ninguna imagen.')

    def clasificar(self, patron) -> str:
        """
            Cálcula las distancias del patrón seleccionado en la
            imágen con respecto a los centroides de las 3 regiones,
            luego compara las distancias para encontrar la menor y
            asignar la clase correspondiente.

            Parámetros:
            patron: Arreglo numpy de los componentes RGB de un pixel

            Retorno:
            Cadena indicando la clase asignada:
            C1: Clase cielo
            C2: Clase pasto
            C3: Clase tierra
        """

        clase_asignada = ""

        d_c1 = distancia_euclidiana(patron, (203, 212, 218))
        d_c2 = distancia_euclidiana(patron, (102, 92, 41))
        d_c3 = distancia_euclidiana(patron, (181, 146, 109))

        if d_c1 > d_c2 > d_c3 or d_c2 > d_c1 > d_c3:
            clase_asignada = "El patrón pertenece a la clase C3"
        elif d_c1 > d_c3 > d_c2 or d_c3 > d_c1 > d_c2:
            clase_asignada = "El patrón pertenece a la clase C2"
        elif d_c3 > d_c2 > d_c1 or d_c2 > d_c3 > d_c1:
            clase_asignada = "El patrón pertenece a la clase C1"

        return clase_asignada

    def evento_manual(self) -> None:
        """
            Obtiene el componente RGB que digita el usuario, lo procesa
            llamando al método clasificar y luego lanza una ventana 
            emergente con texto indicando al usuario que clase fue 
            asignada al patrón que digitó.
        """

        try:
            red = float(self.e_red.get())
            green = float(self.e_green.get())
            blue = float(self.e_blue.get())

            patron = np.array( (red, green, blue) )

            clase = self.clasificar(patron)

            messagebox.showinfo(
                'Clasificación',
                clase
            )
        except:
            messagebox.showerror('Error de valor', 'Ingrese un valor válido RGB.')

    def m_event(self, event, x, y, flags, params) -> None:
        """
            Detecta cuando se ha hecho un clic en la imágen,
            y según las coordenadas extrae los componentes RGB,
            los procesa con el método clasificar, y finalmente 
            imprime en consola la clase asignada.

            Parámetros:
            event: Evento detectado
            x: coordenada x del pixel seleccionado
            y: coordenada y del pixel seleccionado
            flags: Condición específica cuando ocurre un evento del mouse
            params: datos de usuario que se pasan cuando se devuelve la llamada
        """

        # Evento con mouse, descomentar uno de los dos
        #if event == cv2.EVENT_MOUSEMOVE:

        # Evento con clic
        if event == cv2.EVENT_LBUTTONDOWN:
            b = self.img[y, x, 0]
            g = self.img[y, x, 1]
            r = self.img[y, x, 2]
            print(r, g, b)

            patron = np.array( (r, g, b) )

            print(self.clasificar(patron))
            
            cv2.imshow('image', self.img)

    def trabajar_imagen(self) -> None:
        """
            Abre la imágen indicada por la ruta relativa para luego
            mostrarla al usuario en un bucle infinito hasta que decida
            cerrarla, y espera a que el vento de clic ocurra.
        """

        self.img = cv2.imread(self.dir_img, 1)
    
        cv2.imshow('image', self.img)
    
        cv2.setMouseCallback('image', self.m_event)
    
        cv2.waitKey(0)
    
        cv2.destroyAllWindows()

if __name__ == "__main__":
    DistanciaEuclidiana()
