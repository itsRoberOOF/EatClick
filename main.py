from kivy.app import App  # Importa la clase base para crear una aplicación Kivy.
from kivy.uix.screenmanager import ScreenManager, Screen  # Maneja múltiples pantallas.
from kivy.lang import Builder  # Permite cargar archivos de diseño (.kv).
from kivy.uix.boxlayout import BoxLayout  # Importa un contenedor con disposición vertical u horizontal.
from kivy.uix.button import Button  # Importa un botón para la interfaz.
from kivy.uix.label import Label  # Importa una etiqueta de texto.

# ! Importacion de librerias para conectar con firebase
import firebase_admin;
from firebase_admin import credentials, storage;
from firebase_admin import firestore;

# ! Importacion de libreria para manejo de archivos
from pathlib import Path;

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

"""
? Path(__file__).parent → Obtiene la ruta del archivo de python que se esta ejecutando

A esa ruta se le anexa el nombre del archivo JSON para obtener la ruta completa
"""
ruta = Path(__file__).parent / 'proyectopython-4d75d-firebase-adminsdk-4z47o-42798a8811.json';

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

productos = db.collection('productos').stream();

print(productos);

# * Se crea una lista vacia para almacenar los productos
data_productos = [];

# * Se iteran los productos para guardar su informacion, además se convierte el objeto a un diccionario
for producto in productos:
    info_producto = producto.to_dict();
    info_producto['id'] = producto.id;
    data_productos.append(info_producto);

print(data_productos);

# Prueba con imagenes
prueba = storage.bucket();
blob = prueba.get_blob("papas.jpg");
print(blob);

# * Se cierra la conexion
db.close();