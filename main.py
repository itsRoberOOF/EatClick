from kivy.app import App  # Importa la clase base para crear una aplicación Kivy.
from kivy.uix.screenmanager import ScreenManager, Screen  # Maneja múltiples pantallas.
from kivy.lang import Builder  # Permite cargar archivos de diseño (.kv).
from kivy.uix.button import Button  # Importa un botón para la interfaz.
from kivy.uix.image import Image, CoreImage
from kivy.core.window import Window  # Importar la clase Window
from kivy.uix.boxlayout import BoxLayout

import api

Window.size = (400, 600)  # Ancho: 400, Alto: 300

cliente = "";
productos = [];

# Define nuestras diferentes pantallas
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
        data_producto = api.leer_producto(self.id);
        print(data_producto);
        if(data_producto['imagen'] != None):
            img = CoreImage(data_producto['imagen'], ext="png").texture;
            self.ids.imagen_producto.texture = img;

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

