from kivy.app import App  # Importa la clase base para crear una aplicación Kivy.
from kivy.uix.screenmanager import ScreenManager, Screen  # Maneja múltiples pantallas.
from kivy.lang import Builder  # Permite cargar archivos de diseño (.kv).
from kivy.uix.button import Button  # Importa un botón para la interfaz.
from kivy.uix.image import Image, CoreImage
from kivy.core.window import Window  # Importar la clase Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import CardTransition

from winotify import Notification, audio

from copy import deepcopy;

from pathlib import Path;

import api

Window.size = (400, 600)  # Ancho: 400, Alto: 300

cliente = "";
productos = [];

ruta_archivo = Path(__file__).parent / 'Logo_notis.png';

def mostrar_error(msgp:str):
    toast = Notification(app_id="EatClick", title="Error", msg=msgp, duration="short", icon=ruta_archivo);
    toast.set_audio(audio.Reminder, loop=False);
    toast.show();

# Define nuestras diferentes pantallas
class FirstWindow(Screen):
    def enviar_nombre(self):
        # Accede al texto del TextInput
        nombre = self.ids.nombre_input.text;
        if(nombre == "" or len(nombre) < 2):
            mostrar_error("Ingrese un nombre válido");
            return;
        else:
            # Pasa el nombre a la segunda pantalla
            self.manager.get_screen("second").actualizar_label(nombre);
            self.manager.current = "second";

class SecondWindow(Screen):
    def actualizar_label(self, nombre):
        # Actualiza el texto del Label en la pantalla 2
        self.ids.nombre_label.text = f"{nombre}";
        
    def on_enter(self):
        scrollview = self.ids.layout.parent  # Parent del GridLayout es el ScrollView
        scroll_y = scrollview.scroll_y  # Guardar posición actual del scroll
        
        # Limpiar widgets previos
        self.ids.layout.clear_widgets() # Limpia los widgets actuales

        data_categorias = api.leer_coleccion('categorias');
        data_categorias = api.imagenes_coleccion(data_categorias);

        # Mostrar productos con botones para seleccionar
        for categoria in data_categorias:
            nombre = categoria['nombre_categoria'];
            imagen = categoria['imagen'];

            boton_layout = BoxLayout(orientation="vertical");

            if(imagen!=None):
                img = CoreImage(imagen, ext="png").texture;
                widget_imagen = Image(source = "loguito.png", size_hint=(1,0.7), allow_stretch=True, keep_ratio=False);
                widget_imagen.texture = img;
                widget_imagen.text = nombre;
                widget_imagen.bind(on_touch_down=lambda instance, touch, nombre=nombre: self.boton_presionado(instance, touch, nombre))
                boton_layout.add_widget(widget_imagen);

            boton = Button(text=f"{nombre}",size_hint=(1,0.3),background_normal="", background_down="", background_color=(16/255, 67/255, 110/255, 1), font_size=17, halign="center", valign="middle");
            boton.bind(on_press=lambda instance, nombre=nombre: self.boton_presionado(instance, None, nombre))
            boton_layout.add_widget(boton);

            self.ids.layout.add_widget(boton_layout)

        scrollview.scroll_y = scroll_y
            
    def boton_presionado(self, instance, touch, nombre):
        if touch:
            if not instance.collide_point(*touch.pos):
                return  

        # Pasa el nombre a la segunda pantalla
        self.manager.current = "third";
        self.manager.get_screen("third").actualizar_label_categoria(nombre)

class ThirdWindow(Screen):
    def actualizar_label_categoria(self, categoriap):
        self.categoria = categoriap;
        # Actualiza el texto del Label en la pantalla 2
        self.ids.categoria_label.text = f"{self.categoria}";

    def on_enter(self):
        scrollview = self.ids.layout.parent  # Parent del GridLayout es el ScrollView
        scroll_y = scrollview.scroll_y  # Guardar posición actual del scroll
        
        # Limpiar widgets previos
        self.ids.layout.clear_widgets() # Limpia los widgets actuales

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
                widget_imagen = Image(source = "loguito.png", size_hint=(1,0.7), allow_stretch=True, keep_ratio=False);
                widget_imagen.texture = img;
                widget_imagen.text = nombre;
                widget_imagen.bind(on_touch_down=lambda instance, touch, id=id: self.boton_presionado(instance, touch, id))
                boton_layout.add_widget(widget_imagen);
    
            # Crear el botón con formato para el texto
            boton = Button(size_hint=(1, 0.3), background_normal="", background_down="", background_color=(16/255, 67/255, 110/255, 1), font_size=17, halign="center", valign="middle");

            # Habilitar el uso de formato para el texto
            boton.markup = True  # Activar markup
            boton.text = f"[b]{nombre}[/b]\n${precio:,.2f}"  # Formato de texto: nombre en negrita, precio con formato
            
            boton.bind(on_press=lambda instance, id=id: self.boton_presionado(instance, None, id))

            # Añadir el botón al layout
            boton_layout.add_widget(boton)
    
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
        print(self.id);

    def on_enter(self):
        self.ids.input_cantidad.text = "1";

        data_producto = api.leer_producto(self.id);
        self.ids.texto_producto.text = f"{data_producto['nombre']} - ${data_producto['precio']:,.2f}";
        if(data_producto['imagen'] != None):
            img = CoreImage(data_producto['imagen'], ext="png").texture;
            self.ids.imagen_producto.texture = img;
        self.ids.texto_descripcion.text = data_producto['descripcion'];
        self.ids.boton_enviar.bind(on_press=self.agregar_producto);
    
    def agregar_producto(self, instance):
        data_producto = api.leer_producto(self.id);
        validar = self.validar_cantidad();
        if(validar):
            cantidad = int(self.ids.input_cantidad.text);
            data_producto['cantidad'] = cantidad;
            productos.append(data_producto);
            self.validar_productos_duplicados();
            self.manager.current = "third";
    

    def validar_productos_duplicados(self):
        productos_duplicados = [];
        for i, p in enumerate(productos):
            print("Id producto:" + p['id']);
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
            mostrar_error("La cantidad debe estar entre 1 y 99");
        self.ids.input_cantidad.text = str(cantidad);

    def validar_cantidad(self):
        try:
            cantidad = int(self.ids.input_cantidad.text);
            if(cantidad <= 0):
                self.ids.input_cantidad.text = "1";
                mostrar_error("La cantidad debe ser mayor a 0");
                return False;
            elif(cantidad > 99):
                self.ids.input_cantidad.text = "99";
                mostrar_error("La cantidad no puede ser mayor a 99");
                return False;
            else:
                return True;
        except:
            mostrar_error("Ingrese un número válido");
            return False;

# Gestor de pantallas
class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = CardTransition(direction='right');

# Designar archivo de diseño .kv
kv = Builder.load_file('main.kv')

class Eatclick(App):
    def build(self):
        self.icon = str(ruta_archivo);
        return kv;

if __name__ == '__main__':
    Eatclick().run()