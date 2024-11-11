from kivy.app import App  # Importa la clase base para crear una aplicación Kivy.
from kivy.uix.screenmanager import ScreenManager, Screen  # Maneja múltiples pantallas.
from kivy.lang import Builder  # Permite cargar archivos de diseño (.kv).
from kivy.uix.boxlayout import BoxLayout   # Importa un contenedor con disposición vertical u horizontal.
from kivy.uix.button import Button  # Importa un botón para la interfaz.
from kivy.uix.label import Label  # Importa una etiqueta de texto.
from kivy.uix.image import Image, CoreImage

import io

# ! Importacion de librerias para conectar con firebase
import firebase_admin;
from firebase_admin import credentials, storage;
from firebase_admin import firestore;

# ! Importacion de libreria para manejo de archivos
from pathlib import Path;

"""
? Path(__file__).parent → Obtiene la ruta del archivo de python que se esta ejecutando

A esa ruta se le anexa el nombre del archivo JSON para obtener la ruta completa
"""
ruta = Path(__file__).parent / 'proyectopython-4d75d-firebase-adminsdk-4z47o-67a889441f.json';

# Se usa la ruta del archivo JSON para cargar las credenciales
firebase_sdk = credentials.Certificate(ruta)

# Iniciar la app con las credenciales
firebase_admin.initialize_app(firebase_sdk, { 'storageBucket' : 'proyectopython-4d75d.appspot.com' });

# * Conexión con la base
db = firestore.client();

""" 
? db.collection('productos').stream() → Obtiene todos los documentos de la coleccion productos

Crea un objeto de firestore que almacena todos los productos
"""

categorias = db.collection('categorias').stream();

print(categorias);

# * Se crea una lista vacia para almacenar las categorías
data_categorias = [];

# * Se iteran las categorías para guardar su informacion, además se convierte el objeto a un diccionario
for categoria in categorias:
    info_categoria = categoria.to_dict();
    info_categoria['id'] = categoria.id;
    data_categorias.append(info_categoria);

print(data_categorias);

# ! Variable para acceder al storage de firebase
almacenamiento_imagenes = storage.bucket();

# Define nuestras diferentes pantallas
#Define our different screens
class FirstWindow(Screen):
	pass

class SecondWindow(Screen):
    def on_enter(self):
        self.clear_widgets();  # Limpia los widgets actuales
        layout = BoxLayout(orientation='vertical');

        # Mostrar productos con botones para seleccionar
        for categoria in data_categorias:
            nombre = categoria['nombre_categoria'];
            imagen = categoria.get('imagen_categoria', None);
            boton_layout = BoxLayout(orientation='horizontal');
            widget_imagen = None;
            if imagen != None:
                blob = almacenamiento_imagenes.blob(imagen).download_as_bytes();
                bytes = io.BytesIO(blob);
                img = CoreImage(bytes, ext='png').texture;
                print(f"Esta es la imagen {img}");
                widget_imagen = Image(texture=img, size_hint=(0.3, 1), allow_stretch=True, keep_ratio=False);

            if widget_imagen != None:
                boton_layout.add_widget(widget_imagen);
            boton = Button(text=f"{nombre}", size_hint=(0.7, 1));
            boton_layout.add_widget(boton);

            layout.add_widget(boton_layout);

        self.add_widget(layout);

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

