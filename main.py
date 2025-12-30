from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle
from impostor_ips import generar_partida

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.49, 0.0, 0.247, 1) #7D003F
            self.bg = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        

class ImpostorApp(App):

    def build(self):
        self.asignacion = list()
        self.jugador_actual = 0

        self.root = MainScreen(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(20)
        )

        self.pantalla_inicio()
        return self.root
    
    def pantalla_inicio(self):
        self.root.clear_widgets()
        
        logo = Image(
            source="logo.png",
            size_hint_y=0.4,
            allow_stretch=True,
            keep_ratio=True
        )

        titulo = Label(
            text="Impostor IPS",
            font_size=sp(32),
            size_hint_y=0.3
        )
        
        self.input_jugadores = TextInput(
            hint_text="Cantidad de jugadores",
            input_filter="int",
            multiline=False,
            font_size=sp(24),
            size_hint_y=0.2
        )

        self.input_impostores = TextInput(
            hint_text="Cantidad de impostores",
            input_filter="int",
            multiline=False,
            font_size=sp(24),
            size_hint_y=0.2
        )

        boton_jugar = Button(
            text="Jugar",
            font_size=sp(28),
            size_hint_y=0.3
        )
        boton_jugar.bind(on_press=self.iniciar_juego)
        
        self.label_error = Label(
            text="",
            font_size=sp(18),
            size_hint_y=None,
            height=dp(60),
            text_size=(self.root.width - dp(40), None),
            halign="center",
            valign="middle"
        )

        self.root.add_widget(logo)
        self.root.add_widget(titulo)
        self.root.add_widget(self.input_jugadores)
        self.root.add_widget(self.input_impostores)
        self.root.add_widget(boton_jugar)
        self.root.add_widget(self.label_error)
        self.label_error.bind(
            width=lambda *_: self.label_error.setter(
                'text_size'
            )(self.label_error, (self.label_error.width, None))
        )

    def iniciar_juego(self, instance):
        # Validar inputs vacíos
        if not self.input_jugadores.text or not self.input_impostores.text:
            self.label_error.text = "Completá todos los campos"
            return

        jugadores = int(self.input_jugadores.text)
        impostores = int(self.input_impostores.text)

        # Validaciones lógicas
        if jugadores <= 0:
            self.label_error.text = "Debe haber al menos 1 jugador"
            return

        if impostores <= 0:
            self.label_error.text = "Debe haber al menos 1 impostor"
            return

        if impostores >= jugadores:
            self.label_error.text = "El número de impostores debe ser menor al de jugadores"
            return

        # Si todo está bien, limpiar error y arrancar
        self.label_error.text = ""

        self.asignacion = generar_partida(jugadores, impostores)
        self.jugador_actual = 0

        self.mostrar_jugador()

    def mostrar_jugador(self):
        self.root.clear_widgets()

        label = Label(
            text=f"Jugador {self.jugador_actual + 1}",
            font_size=sp(36),
            size_hint_y=0.6
        )

        boton_ver = Button(
            text="Ver palabra",
            font_size=sp(28),
            size_hint_y=0.4
        )
        boton_ver.bind(on_press=self.ver_palabra)

        self.root.add_widget(label)
        self.root.add_widget(boton_ver)

    def ver_palabra(self, instance):
        self.root.clear_widgets()

        palabra = self.asignacion[self.jugador_actual]

        label = Label(
            text=palabra,
            font_size=sp(42),
            size_hint_y=0.6
        )

        boton_siguiente = Button(
            text="Siguiente",
            font_size=sp(28),
            size_hint_y=0.4
        )
        boton_siguiente.bind(on_press=self.siguiente)

        self.root.add_widget(label)
        self.root.add_widget(boton_siguiente)

    def siguiente(self, instance):
        self.jugador_actual += 1

        if self.jugador_actual < len(self.asignacion):
            self.mostrar_jugador()
        else:
            self.fin_juego()

    def fin_juego(self):
        self.root.clear_widgets()

        label = Label(
            text="Fin del juego",
            font_size=sp(32),
            size_hint_y=0.6
        )

        boton_restart = Button(
            text="Jugar otra vez",
            font_size=sp(28),
            size_hint_y=0.4
        )
        boton_restart.bind(on_press=self.reiniciar)

        self.root.add_widget(label)
        self.root.add_widget(boton_restart)

    def reiniciar(self, instance):
        self.asignacion = list()
        self.jugador_actual = 0
        self.pantalla_inicio()


ImpostorApp().run()