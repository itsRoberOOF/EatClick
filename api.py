
# * Archivo para manejar las funciones que conectan con la base de datos

# ! Importacion de librerias para conectar con firebase
import firebase_admin;
from firebase_admin import credentials, storage;
from firebase_admin import firestore;

# ! Importacion de libreria para manejo de archivos
from pathlib import Path;

import io;

"""
? Path(__file__).parent → Obtiene la ruta del archivo de python que se esta ejecutando

A esa ruta se le anexa el nombre del archivo JSON para obtener la ruta completa
"""
ruta = Path(__file__).parent / 'proyectopython-4d75d-firebase-adminsdk-4z47o-67a889441f.json';

# Se usa la ruta del archivo JSON para cargar las credenciales
firebase_sdk = credentials.Certificate(ruta)

# Iniciar la app con las credenciales
firebase_admin.initialize_app(firebase_sdk, { 'storageBucket' : 'proyectopython-4d75d.appspot.com' });

# ! Variable para acceder al storage de firebase
almacenamiento_imagenes = storage.bucket();

def leer_coleccion(nombre_coleccion:str):
    try:
        # * Conexión con la base
        db = firestore.client();

        """ 
        ? db.collection().stream() → Obtiene todos los documentos de la coleccion indicada

        Crea un objeto de firestore que almacena todos los productos
        """

        documentos = db.collection(nombre_coleccion).stream();

        # * Se crea una lista vacia para almacenar los documentos
        data_documentos = [];

        # * Se iteran los documentos para guardar su informacion, además se convierte el objeto a un diccionario
        for documento in documentos:
            info_doc = documento.to_dict();
            info_doc['id'] = documento.id;
            data_documentos.append(info_doc);

        # ! Se cierra la conexión con la base
        db.close();

        # Retorno
        return data_documentos;
    except:
        print("Error en la base de datos");
        return None;

def imagenes_coleccion(diccionario:dict):
    try:
        data_documentos = diccionario;

        for doc in data_documentos:
            imagen = doc.get('imagen', None);

            if(imagen != None):
                blob = almacenamiento_imagenes.blob(imagen).download_as_bytes();
                bytes = io.BytesIO(blob);
                doc['imagen'] = bytes;
            else:
                doc['imagen'] = None;

        return data_documentos;
    except:
        print("Error en la base de datos");
        return None;

def leer_productos(categoria:str):
    try:
        data_productos = leer_coleccion("productos");
        productos_filtrados = [];
        for i in data_productos:
            if(i['categoria'] == categoria):
                productos_filtrados.append(i);
        return productos_filtrados;
    except:
        print("Error en la base de datos");
        return None;

def leer_producto(id:str):
    try:
        data_productos = leer_coleccion("productos");
        for i in data_productos:
            if(i['id'] == id):
                imagen = i.get('imagen', None);
                if(imagen != None):
                    blob = almacenamiento_imagenes.blob(imagen).download_as_bytes();
                    bytes = io.BytesIO(blob);
                    i['imagen'] = bytes;
                else:
                    i['imagen'] = None;
                return i;
    except:
        print("Error en la base de datos");
        return None;