
# ! Importacion de librerias para conectar con firebase
import firebase_admin;
from firebase_admin import credentials;
from firebase_admin import firestore;

from pathlib import Path;

# * Cargar las credenciales de firebase desde el JSON

"""

"""
ruta = Path(__file__).parent / 'eatclick-1-firebase-adminsdk-1zv5v-3b3b3b3b3b.json';
print(ruta);

firebase_sdk = credentials.Certificate(ruta)
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

