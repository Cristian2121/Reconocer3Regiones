"""
    Título del proyecto: GUI K-NN CON DISTANCIA MÍNIMA
    Descripción del proyecto: Permite seleccionar una imágen, y clasificarla según el método k-NN con distancia mínima.
    Autor: Cristian Del Angel Fiscal
    Fecha: 25/12/2022
    Licencia: Ninguna

    Librerías:
    tkinter: Kit de herramientas GUI.
    cv2: Abrir imágen y extraer RGB de pixel seleccionado
    numpy: Convertir valores RGB en vector numpy para fácil operación de vectores
    dis_euclidiana: Implementación del algoritmo de distancia euclidiana
    trabajar_csv: Para recuperar el conjunto de datos correspondientes al algoritmo K-NN
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox

import cv2
import numpy as np

from dis_euclidiana import distancia_euclidiana
from trabajar_csv import ArchivoCSV

class KNNDisMin():
    """
        Interfaz Gráfica de Usuario que permite seleccionar una imágen para extraer
        los componentes RGB de un pixel, para posteriormente procesarlo con la técnica
        de clasificación K-NN con distancia mínima, y enviar una respuesta al usuario final.
    """

    def __init__(self) -> None:
        """
            Constructor de la clase.
        """

        nueva_ventana = Tk()
        nueva_ventana.title('KNN Distancia Mínima')

        #------------- VARIABLES GLOBALES -------------
        self.dir_img = StringVar()

        frm_principal = ttk.Frame(nueva_ventana)
        frm_principal.pack()

        l_titulo = ttk.Label(
            frm_principal, 
            text="""
                Análisis con el método K-NN: \n
                Distancia Mínima
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
            Obtiene el conjunto de datos de clasificaciones pasadas, cálcula
            las distancias euclidianas de todos esos elementos con respecto al
            nuevo patrón RGB, almacena las distancias y su clase asignada, y luego
            ordena de menor a mayor esos elementos, para así tomar el primero 
            (más pequeño) y asignarle la misma clase al nuevo patrón, el cual lo 
            almacena como nuevo elemento en el conjunto de datos del archivo csv.

            Parámetros:
            patron: Arreglo numpy de los componentes RGB de un pixel

            Retorno:
            Cadena indicando la clase asignada:
            C1: Clase cielo
            C2: Clase pasto
            C3: Clase tierra
        """

        clase_asignada = ""

        lista_dis_clase = []
        datos = ArchivoCSV().leer_datos()

        # Se recorre la lista de diccionarios para calcular la distancia del nuevo patrón con los anteriores.
        for fila in datos:
            # Primero convertimos los datos del diccionario a enteros para poder trabajarlos.
            dis_fila = distancia_euclidiana((int(fila['R']), int(fila['G']), int(fila['B'])), (patron[0], patron[1], patron[2]))
            dicc_fila = {'dis':dis_fila, 'clase':int(fila['CLASE'])}

            # Agregamos las distancias y sus clases a una lista nueva
            lista_dis_clase.append(dicc_fila)

        # Ordenamiento de la lista de diccionarios a partir de la llave con el valor de las distancias
        lista_ordenada = sorted(lista_dis_clase, key=lambda d: d['dis'])

        clase_numero = lista_ordenada[0]['clase']

        if clase_numero == 1:
            clase_asignada = "El patrón pertenece a la clase C1"
        elif clase_numero == 2:
            clase_asignada = "El patrón pertenece a la clase C2"
        elif clase_numero == 3:
            clase_asignada = "El patrón pertenece a la clase C3"

        # Nuevo diccionario que se agregará al archivo con la información del nuevo patrón.
        dicc_nuevo = {
            # Obtenemos el último item de la lista y aumentamos el contador de casos.
            'CASO':int(datos[-1]['CASO']) + 1, 
            'R':patron[0],
            'G':patron[1],
            'B':patron[2],
            # K-NN con distancia mínima clasifica al patrón en la clase de la distancia más pequeña.
            'CLASE':clase_numero
        }

        ArchivoCSV().escribir_dato(dicc_nuevo)

        return clase_asignada

    def evento_manual(self) -> None:
        """
            Obtiene el componente RGB que digita el usuario, lo procesa
            llamando al método clasificar y luego lanza una ventana 
            emergente con texto indicando al usuario que clase fue 
            asignada al patrón que digitó.
        """

        try:
            red = int(self.e_red.get())
            green = int(self.e_green.get())
            blue = int(self.e_blue.get())

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
    KNNDisMin()