from kivy.app import App  # Importa la clase base para crear una aplicación Kivy.
from kivy.uix.screenmanager import ScreenManager, Screen  # Maneja múltiples pantallas.
from kivy.lang import Builder  # Permite cargar archivos de diseño (.kv).
from kivy.uix.boxlayout import BoxLayout  # Importa un contenedor con disposición vertical u horizontal.
from kivy.uix.button import Button  # Importa un botón para la interfaz.
from kivy.uix.label import Label  # Importa una etiqueta de texto.

# Define nuestras diferentes pantallas
#Define our different screens
class FirstWindow(Screen):
	pass

class SecondWindow(Screen):
     def on_enter(self):
        self.clear_widgets()  # Limpia los widgets actuales
        layout = BoxLayout(orientation='vertical')

        # Agregar un producto a la lista 
        productos = [
            {"nombre": "Manzana", "precio": 1.50},
            {"nombre": "Pan", "precio": 0.80},
            {"nombre": "Leche", "precio": 1.20},
            {"nombre": "Huevo", "precio": 2.00}
        ]

        # Mostrar productos con botones para seleccionar
        for producto in productos:
            nombre = producto['nombre']
            precio = producto['precio']
            boton = Button(text=f"{nombre} - ${precio:.2f}", size_hint=(1, 0.1))
            layout.add_widget(boton)

        self.add_widget(layout)

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
