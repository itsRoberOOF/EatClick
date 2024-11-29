import datetime
from logging import root
import os
import random
from fpdf import FPDF # Para poder generar el PDF de la factura.
from kivy.app import App  # Importa la clase base para crear una aplicación Kivy.
from kivy.uix.screenmanager import ScreenManager, Screen  # Maneja múltiples pantallas.
from kivy.lang import Builder  # Permite cargar archivos de diseño (.kv).
from kivy.uix.button import Button  # Importa un botón para la interfaz.
from kivy.uix.image import Image, CoreImage
from kivy.core.window import Window  # Importar la clase Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import CardTransition
from kivy.uix.label import Label

from winotify import Notification, audio # Permite generar las notificaciones en la pantalla

from pathlib import Path;

import api

# Para las medidas de la pantalla:
Window.size = (400, 600)  # Ancho: 400, Alto: 300

cliente = ""; # Es para guardar el nombre del cliente
productos = []; # Para guardar la lista de productos que se van a pedir

#
ruta_imagenes = Path(__file__).parent;

# Esta función permite que se muestren las notificaciones para el usuario
# Recibe los parametros de "titulop" y "msgp", titulop es el titulo de la notificacion y msgp es el mensaje que se mostrará
def mostrar_noti(titulop:str, msgp:str): #Ambos parámetros son strings
    # Configurar la notifación
    toast = Notification(app_id="EatClick", title=titulop, msg=msgp, duration="short", icon=str(ruta_imagenes / "Logo_notis.png"));
    # Establecer el sonido de la notificación
    toast.set_audio(audio.Reminder, loop=False);
    # Mostrar la notificación
    toast.show();

# Esta clase define la primera pantalla dentro de la aplicación (donde se encuentra el logo y el input para ingresar el nombre del usuario)
class FirstWindow(Screen):
    def enviar_nombre(self):
        # Accede al texto del TextInput
        nombre = self.ids.nombre_input.text;
        global cliente; #Se accede a la variable fuera de la clase para poder trabajarla
        cliente = nombre #nombre almacenado en variable global
        if(nombre == "" or len(nombre) < 2): #Para validar el nombre
            mostrar_noti("Error", "Ingrese un nombre válido (mayor a 2 caracteres)"); #Por si el nombre ingresado no es correcto
            return;
        else:
            # Pasa el nombre a la segunda pantalla
            self.manager.get_screen("second").actualizar_label(nombre);
            self.manager.current = "second";
    
    # 
    def on_leave(self):
        self.ids.nombre_input.text = "";

# Esta clase define la segunda pantalla dentro de la aplicación (donde se encuentra el menú)
class SecondWindow(Screen):
    # Esta función actualiza el texto del Label en la pantalla 2 para que tenga el nombre que fue ingresado en la pantalla 1
    # Recibe el parámetro de nombre
    def actualizar_label(self, nombre):
        self.ids.nombre_label.text = f"{nombre}";

    # Esta función permite que se pueda entrar a uno de los productos del menú
    def on_enter(self):
        # Para que no se dé click al intentar dar scroll
        scrollview = self.ids.layout.parent;
        scroll_y = scrollview.scroll_y;
        
        # Limpiar widgets previos
        self.ids.layout.clear_widgets();

        # Para acceder a la información de la base de datos
        data_categorias = api.leer_coleccion('categorias');
        data_categorias = api.imagenes_coleccion(data_categorias);

        # Mostrar productos con botones para seleccionar
        for categoria in data_categorias:
            nombre = categoria['nombre_categoria']; # Se encuentra en la base de datos
            imagen = categoria['imagen']; # Son las imágenes de los productos

            # Se crea un layout para organizar los elementos de la parte superior
            boton_layout = BoxLayout(orientation="vertical");

            if(imagen!=None):
                # Convierte la imagen para que se cargue correctamente (Se crea una textura)
                img = CoreImage(imagen, ext="png").texture;
                # Crea un widget para alojar ahí la imagen
                widget_imagen = Image(source = "", size_hint=(1,0.7), allow_stretch=True, keep_ratio=False);
                # Asigna la textura a la imagen
                widget_imagen.texture = img;

                # Permite que se pueda dar click a la imagen
                widget_imagen.bind(on_touch_down=lambda instance, touch, nombre=nombre: self.boton_presionado(instance, touch, nombre));
                boton_layout.add_widget(widget_imagen);
            
            #Crea un espacio en blanco luego de escribir el nombre
            boton = Button(text=f"{nombre}",size_hint=(1,0.3),background_normal="", background_down="", background_color=(16/255, 67/255, 110/255, 1), font_size=17, halign="center", valign="middle");
            #Permite que se pueda presionar el botón del carrito
            boton.bind(on_press=lambda instance, nombre=nombre: self.boton_presionado(instance, None, nombre));
            boton_layout.add_widget(boton);

            #Agrega el widget de la imagen al layout
            self.ids.layout.add_widget(boton_layout);
        
        # Permite que se mantenga la posición del scroll
        scrollview.scroll_y = scroll_y;

    # Esta función permite que se pueda         
    def boton_presionado(self, instance, touch, nombre):
        if touch:
            if not instance.collide_point(*touch.pos): # para determinar que la posición del toque está dentro del widget
                return;

        # Pasa a la tercera pantalla según la categoría seleccionada
        self.manager.current = "third";
        self.manager.get_screen("third").actualizar_label_categoria(nombre)

class ThirdWindow(Screen):
    def actualizar_label_categoria(self, categoriap):
        self.categoria = categoriap;
        # Actualiza el texto de la categoria
        self.ids.categoria_label.text = f"{self.categoria}";

    def on_enter(self):
        scrollview = self.ids.layout.parent;
        scroll_y = scrollview.scroll_y;
        
        # Limpiar widgets previos
        self.ids.layout.clear_widgets();

        data_productos = api.leer_productos(self.categoria);
        data_productos = api.imagenes_coleccion(data_productos);

        # Mostrar productos con botones para seleccionar
        for producto in data_productos:
            id = producto['id'];
            nombre = producto['nombre'];
            precio = producto['precio'];
            imagen = producto['imagen'];

            boton_layout = BoxLayout(orientation="vertical");

            if(imagen!=None):
                img = CoreImage(imagen, ext="png").texture;
                widget_imagen = Image(source = "", size_hint=(1,0.7), allow_stretch=True, keep_ratio=False);
                widget_imagen.texture = img;
                widget_imagen.bind(on_touch_down=lambda instance, touch, id=id: self.boton_presionado(instance, touch, id));
                boton_layout.add_widget(widget_imagen);
    
            # Crear el botón con formato para el texto
            boton = Button(size_hint=(1, 0.3), background_normal="", background_down="", background_color=(16/255, 67/255, 110/255, 1), font_size=17, halign="center", valign="middle");

            # Habilitar el uso de formato para el texto
            boton.markup = True;
            boton.text = f"[b]{nombre}[/b]\n${precio:,.2f}";
            
            boton.bind(on_press=lambda instance, id=id: self.boton_presionado(instance, None, id));

            # Añadir el botón al layout
            boton_layout.add_widget(boton);
    
            self.ids.layout.add_widget(boton_layout);
        
        scrollview.scroll_y = scroll_y;

    def boton_presionado(self, instance, touch, id):
        if touch:
            if not instance.collide_point(*touch.pos):
                return;
        self.manager.current = "fourth";
        self.manager.get_screen("fourth").recibir_id(id);

class FourthWindow(Screen):
    def recibir_id(self, idp):
        self.id = idp;

    def on_enter(self):
        self.ids.input_cantidad.text = "1";

        data_producto = api.leer_producto(self.id);
        self.ids.texto_producto.text = f"{data_producto['nombre']} - ${data_producto['precio']:,.2f}";

        if(data_producto['imagen'] != None):
            img = CoreImage(data_producto['imagen'], ext="png").texture;
            self.ids.imagen_producto.texture = img;
        else:
            self.ids.imagen_producto.source = str(ruta_imagenes / "Default.png");
        
        self.ids.texto_descripcion.text = data_producto['descripcion'];
        self.ids.boton_enviar.bind(on_press=self.agregar_producto);
    
    def on_leave(self):
        self.ids.imagen_producto.texture = None;
        self.ids.imagen_producto.source = str(ruta_imagenes / "Default.png");
        self.ids.texto_producto.text = "";
        self.ids.texto_descripcion.text = "";

    def agregar_producto(self, instance):
        data_producto = api.leer_producto(self.id);
        validar = self.validar_cantidad();
        if(validar):
            cantidad = int(self.ids.input_cantidad.text);
            data_producto['cantidad'] = cantidad;
            data_producto['id'] = self.id;
            productos.append(data_producto);
            self.validar_productos_duplicados();
            self.manager.current = "second";
            mostrar_noti("Éxito", "Producto agregado al carrito");
    
    def validar_productos_duplicados(self):
        productos_duplicados = [];
        for i, p in enumerate(productos):
            if(p['id'] == self.id): 
                info_producto = {"posicion": i, "cantidad": p['cantidad']};
                productos_duplicados.append(info_producto);
        
        if(len(productos_duplicados) > 1):
            cantidad_total = 0;
            for i in productos_duplicados:
                cantidad_total += i['cantidad'];
            productos[productos_duplicados[0]['posicion']]['cantidad'] = cantidad_total;
            for i in range(1, len(productos_duplicados)):
                productos.pop(productos_duplicados[i]['posicion']);

    def botones_cantidad(self, operacion:str):
        cantidad = int(self.ids.input_cantidad.text);
        if(operacion == 'suma' and cantidad < 99):
            cantidad = int(cantidad) + 1;
        elif(operacion == 'resta' and cantidad > 1):
            cantidad = int(cantidad) - 1;
        else:
            mostrar_noti("Error", "La cantidad debe estar entre 1 y 99");
        self.ids.input_cantidad.text = str(cantidad);

    def validar_cantidad(self):
        try:
            cantidad = int(self.ids.input_cantidad.text);
            if(cantidad <= 0):
                self.ids.input_cantidad.text = "1";
                mostrar_noti("Error", "Ingrese un número válido (entre 1 y 99)");
                return False;
            elif(cantidad > 99):
                self.ids.input_cantidad.text = "99";
                mostrar_noti("Error", "Ingrese un número válido (entre 1 y 99)");
                return False;
            else:
                return True;
        except:
            mostrar_noti("Error", "Ingrese un número válido (entre 1 y 99)");
            return False;

class FifthWindow(Screen):
    productos_factura = [];

    def on_enter(self):
        self.productos_factura = [];
        scrollview = self.ids.layout.parent;
        scroll_y = scrollview.scroll_y;

        # Limpiar widgets previos
        self.ids.layout.clear_widgets();

        precio_total = 0;

        if len(productos) > 0:
            for i, p in enumerate(productos):
                data_producto = api.leer_producto(p['id']);
                data_producto['cantidad'] = p['cantidad'];
                self.productos_factura.append(data_producto);
                boton_layout = BoxLayout(orientation="horizontal", size_hint=(0.9, None), height=80);
                if data_producto['imagen'] != None:
                    img = CoreImage(data_producto['imagen'], ext="png").texture;
                    widget_imagen = Image(source = "", size_hint=(0.3, 1), allow_stretch=True, keep_ratio=False);
                    widget_imagen.texture = img;
                    boton_layout.add_widget(widget_imagen);

                texto_layout = BoxLayout(orientation="vertical", size_hint=(0.6, 1), pos_hint={"center_y": 0.5}, spacing=0);
                label_info_producto = Label(text=f"{data_producto['nombre']} - ${data_producto['precio']:,.2f}", size_hint=(1, 0.5), font_size=18, bold= True, halign="left", valign="bottom", text_size=(170, None), color=(1, 1, 1, 1));
                label_cantidad = Label(text=f"x{p['cantidad']}", size_hint=(1, 0.5), font_size=16, halign="left", valign="top", text_size=(170, None), color=(174/255, 169/255, 169/255, 1));

                texto_layout.add_widget(label_info_producto);
                texto_layout.add_widget(label_cantidad);

                boton_layout.add_widget(texto_layout);

                ruta_basurero = str(ruta_imagenes / "Boton_basurero.png");
                ruta_basurero_presionado = str(ruta_imagenes / "Boton_basurero_presionado.png");

                boton_basurero = Button(size_hint=(None, None), width=45, height=45, background_normal=ruta_basurero, background_down=ruta_basurero_presionado, pos_hint={"center_y": 0.5});

                boton_basurero.bind(on_press=lambda instance, posicion=i: self.borrar_producto(instance, posicion));

                boton_layout.add_widget(boton_basurero);

                # Agregar el layout principal al contenedor
                self.ids.layout.add_widget(boton_layout);

                precio_total += data_producto['precio'] * p['cantidad'];
            self.ids.precio_total.text = f"${precio_total:,.2f}";
        else:
            label = Label(text="No hay productos en el carrito", font_size=18, color=(1, 1, 1, 1));
            self.ids.layout.add_widget(label);
            self.ids.precio_total.text = "$0.00";
        scrollview.scroll_y = scroll_y;

    def generar_factura(self):
        global cliente;
        if(len(self.productos_factura) > 0):
            numero_orden = random.randint(10000, 99999); #genera un numero de orden random
            fecha_hora_actual = datetime.datetime.now(); #captura la fecha y hora actual
            total = sum(producto['precio'] * producto['cantidad'] for producto in productos); #suma el valor de los productos
            #utilizando libreria para reportes (fpdf
            pdf = FPDF(orientation='P'); #objeto del pd
            pdf.add_page(); #agrega una pagin
            pdf.set_font("Arial", size=12); #fuente
            #Encabezad
            pdf.image(str(ruta_imagenes / "Logo_notis.png"), x=10, y=8, w=30, h=30); #loguito del sistem
            pdf.set_font("Arial", size=16, style='B'); #fuente
            pdf.cell(200, 10, txt="Factura Electrónica - EatClick", ln=1, align='C'); 
            pdf.cell(200, 10, txt=fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"), ln=1, align='C');
            pdf.cell(200, 10, txt=f"Cliente: {cliente} - {numero_orden}", ln=1, align='C'); #cliente que se obtiene de variable global en FirstWindow
            
            pdf.cell(200, 5, txt="", ln=1); #separacion visual
            
            pdf.cell(100, 10, txt="Producto:", ln=0);
            pdf.cell(40, 10, txt="Cantidad:", ln=0);
            pdf.cell(60, 10, txt="Precio Total:", ln=1);
            for producto in productos: #for que recorre la lista de 'productos' y setea los valores con formato
                pdf.cell(100, 10, txt=producto['nombre'], ln=0);
                pdf.cell(40, 10, txt=str(producto['cantidad']), ln=0);
                pdf.cell(60, 10, txt=f"${producto['precio'] * producto['cantidad']:.2f}", ln=1);
                
            pdf.cell(200, 5, txt="", ln=1);
            
        pdf.cell(160, 10, txt="Total:", ln=0);    
        pdf.cell(40, 10, txt=f"${total:.2f}", ln=1); #total de compra
        
        carpeta_facturas = "facturas_restaurante"; #crea la carpeta para almacenar facturas
        if not os.path.exists(carpeta_facturas):
            os.makedirs(carpeta_facturas); #si no existe

        #guarda el archivo y almacena la ruta en la variable
        ruta_archivo = os.path.join(carpeta_facturas, f"factura_{numero_orden}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf");

        pdf.output(ruta_archivo); #guardamos el pdf
        mostrar_noti("Factura creada", "Su factura ha sido creada con éxito!"); #mensaje de exito
        productos.clear();
        cliente = "";
        self.manager.current = 'first'; #regresa al inicio

    def borrar_producto(self, instance, posicion):
        productos.pop(posicion);
        mostrar_noti("Éxito", "Producto eliminado del carrito");
        self.on_enter();

# Gestor de pantallas
class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs);
        self.transition = CardTransition(direction='right');

# Designar archivo de diseño .kv
kv = Builder.load_file('main.kv');

class Eatclick(App):
    def build(self):
        self.icon = str(ruta_imagenes / "Logo_notis.png");
        return kv;

if __name__ == '__main__':
    Eatclick().run();