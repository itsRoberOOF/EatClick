
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

#metodo para leer las colecciones
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

#obtiene las imagenes almacenadas en la base de datos.
def imagenes_coleccion(diccionario:dict): #recibe un directorio como parametro
    try:
        data_documentos = diccionario; #se almacena en una variable el diccionario

        for doc in data_documentos: #se recorre el diccionario
            imagen = doc.get('imagen', None); #obtenemos la imagen

            if(imagen != None): #si la imagen existe...
                blob = almacenamiento_imagenes.blob(imagen).download_as_bytes(); #se descarga la imagen como bytes
                bytes = io.BytesIO(blob); #se convierte a bytes
                doc['imagen'] = bytes; #se reasigna la imagen en bytes al campo del diccionario
            else:
                doc['imagen'] = None; #se setea como vacio

        return data_documentos; #se retorna
    except:
        print("Error en la base de datos");
        return None;

#lee la coleccion de productos: SELECT a productos
def leer_productos(categoria:str):
    try:
        data_productos = leer_coleccion("productos"); #se guarda en una variable la info recolectada
        productos_filtrados = []; #arreglo o lista vacia
        for i in data_productos: #recorremos la data almacenada en la variable
            if(i['categoria'] == categoria): #se evalua que la categoria del producto pertenezca a la que se pasa como parametro
                productos_filtrados.append(i); #se agregan a la lista filtrada
        return productos_filtrados; #se retorna la lista filtrada por categoria
    except:
        print("Error en la base de datos");
        return None;

#lee los productos por ID
def leer_producto(id:str):
    try:
        data_productos = leer_coleccion("productos"); #se guardan las productos en una variable
        for i in data_productos: #se recorre la data
            if(i['id'] == id): #se busca matchear los productos que posean el mismo ID que el que se pasa como parametro
                imagen = i.get('imagen', None); #se obtiene la imagen de los productos que coinciden
                if(imagen != None): #si hay algo almacenado en la variable...
                    blob = almacenamiento_imagenes.blob(imagen).download_as_bytes();
                    bytes = io.BytesIO(blob);
                    i['imagen'] = bytes; #proceso de asignacion de la imagen convertida (mismo proceso que arriba)
                else:
                    i['imagen'] = None; #se setea como vacio
                return i; #retornamos i
    except:
        print("Error en la base de datos");
        return None;