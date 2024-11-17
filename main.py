from kivy.app import App  # Importa la clase base para crear una aplicación Kivy.
from kivy.uix.screenmanager import ScreenManager, Screen  # Maneja múltiples pantallas.
from kivy.lang import Builder  # Permite cargar archivos de diseño (.kv).
from kivy.uix.gridlayout import GridLayout   # Importa un contenedor con disposición vertical u horizontal.
from kivy.uix.button import Button  # Importa un botón para la interfaz.
from kivy.uix.label import Label  # Importa una etiqueta de texto.
from kivy.uix.image import Image, CoreImage
from kivy.core.window import Window  # Importar la clase Window
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Color
from kivy.graphics import Rectangle

import api

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
        self.ids.nombre_label.text = f"{nombre}";
        
    def on_enter(self):
        # Limpiar widgets previos
        self.ids.layout.clear_widgets() # Limpia los widgets actuales

        data_categorias = api.leer_coleccion('categorias');
        data_categorias = api.imagenes_coleccion(data_categorias);

        # Mostrar productos con botones para seleccionar
        for categoria in data_categorias:
            nombre = categoria['nombre_categoria'];
            imagen = categoria['imagen'];
            boton_layout = BoxLayout(orientation='vertical', size_hint=(1,None), height=200);
            
            with boton_layout.canvas.before:
                Color(16/255, 67/255, 110/255, 1)
                Rectangle(pos=boton_layout.pos, size=boton_layout.size)
            boton_layout.bind(pos=lambda instance, value: setattr(instance.canvas.before.children[-1], 'pos', value))
            boton_layout.bind(size=lambda instance, value: setattr(instance.canvas.before.children[-1], 'size', value))
            widget_imagen = None;
            if imagen != None:
                img = CoreImage(imagen, ext='png').texture;
                widget_imagen = Image(texture=img, size_hint=(1, 0.7), allow_stretch=True, keep_ratio=False);

            if widget_imagen != None:
                boton_layout.add_widget(widget_imagen); 

            label = Label(text=nombre, size_hint=(1, 0.2), halign='center', valign='middle', text_size=(None, None));
            boton_layout.add_widget(label);
            self.ids.layout.add_widget(boton_layout)
    
    def on_button_press(self, instance):
        # Esta función se ejecutará cuando se presione el botón
        print(f"Botón presionado: {instance.text}")

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

