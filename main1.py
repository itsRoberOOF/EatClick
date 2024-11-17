from kivy.app import App  # Importa la clase base para crear una aplicación Kivy.
from kivy.uix.screenmanager import ScreenManager, Screen  # Maneja múltiples pantallas.
from kivy.lang import Builder  # Permite cargar archivos de diseño (.kv).
from kivy.uix.boxlayout import BoxLayout  # Importa un contenedor con disposición vertical u horizontal.
from kivy.uix.button import Button  # Importa un botón para la interfaz.
from kivy.uix.label import Label  # Importa una etiqueta de texto.
from kivy.core.window import Window  # Importar la clase Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, CoreImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

Window.size = (400, 600)  # Ancho: 400, Alto: 300
# Define nuestras diferentes pantallas
#Define our different screens
class FirstWindow(Screen):
    def enviar_nombre(self):
        # Accede al texto del TextInput
        nombre = self.ids.nombre_input.text
        # Pasa el nombre a la segunda pantalla
        self.manager.get_screen("second").actualizar_label(nombre)

class SecondWindow(Screen):
    def actualizar_label(self, nombre):
        # Actualiza el texto del Label en la pantalla 2
        self.ids.nombre_label.text = f"Hola, bienvenido {nombre}"
        

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.productos = [
                    {"nombre": "Manzana", "precio": 1.50},
                    {"nombre": "Pan", "precio": 0.80},
                    {"nombre": "Leche", "precio": 1.20},
                    {"nombre": "Huevo", "precio": 2.00},
                    {"nombre": "Manzana", "precio": 1.50},
                    {"nombre": "Pan", "precio": 0.80},
                    {"nombre": "Leche", "precio": 1.20},
                    {"nombre": "Huevo", "precio": 2.00},
                    {"nombre": "Manzana", "precio": 1.50},
                    {"nombre": "Pan", "precio": 0.80},
                    {"nombre": "Leche", "precio": 1.20},
                    {"nombre": "Huevo", "precio": 2.00}
                    
                ]
    
    def on_enter(self):
        # Limpiar widgets previos
        self.ids.layout.clear_widgets()
        
        # Agregar productos como botones
        for producto in self.productos:
            nombre = producto['nombre']
            precio = producto['precio']
            boton = Button(text=f"{nombre} - ${precio:.2f}")
            self.ids.layout.add_widget(boton)  # Agrega el botón al layout

# Gestor de pantallas
class WindowManager(ScreenManager):
    pass

# Designar archivo de diseño .kv
kv = Builder.load_file('main.kv')

class Eatclick(App):
    def build(self):
        return kv

if __name__ == '__main__':
    Eatclick().run()
