
# ! Importacion de librerias para conectar con firebase
import firebase_admin;
from firebase_admin import credentials;
from firebase_admin import firestore;

# * Cargar las credenciales de firebase desde el JSON
firebase_sdk = credentials.Certificate('ProyectoPython/proyectopython-4d75d-firebase-adminsdk-4z47o-42798a8811.json')
# * Iniciar la app con las credenciales
firebase_admin.initialize_app(firebase_sdk);

""" 
! Conexión con la base
? Crea un "cliente" que tiene 
"""
db = firestore.client();


productos = db.collection('productos').stream();

print(productos);

data_productos = [];

for producto in productos:
    info_producto = producto.to_dict();
    info_producto['id'] = producto.id;
    data_productos.append(info_producto);

print(data_productos);

db.close();