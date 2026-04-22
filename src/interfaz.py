import customtkinter as ctk

# fuentes para la interfaz grafica
FUENTE_APP = "Segoe UI"
FUENTE_MONO = "Consolas"

# apaciencia de la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# clase que crea la interfaz grafica
class Interfaz(ctk.CTk):

    # inicializa la interfaz grafica
    def __init__(self, callback_adivinar, callback_inicio,callback_pista):
        super().__init__()
        # titulo de la ventana
        self.title("Ahorcado POO - UNRC")
        # tamaño de la ventana
        self.geometry("800x600")

        # comunicacion con el motor del juego
        self.callback_adivinar = callback_adivinar
        self.callback_inicio = callback_inicio
        self.callback_pista = callback_pista  
        # nombre del jugador en la pantalla
        self.nombre_jugador = None

        # tamaño del contenedor de la app
        self.container = ctk.CTkFrame(self, corner_radius=15)
        self.container.pack(padx=20, pady=20, fill="both", expand=True)

        self.setup_pantalla_inicio()

    # limpia la pantalla
    def limpiar_pantalla(self):
        # elimina todos los elementos del contenedor
        for widget in self.container.winfo_children():
            widget.destroy()

    # pantalla de inicio de la app
    def setup_pantalla_inicio(self):
        self.limpiar_pantalla()

        # titulo de la app
        ctk.CTkLabel(
            self.container, text="AHORCADO POO", font=(FUENTE_APP, 36, "bold")
        ).pack(pady=30)

        # subtitulo de la app
        ctk.CTkLabel(
            self.container, text="Reto Final - 4to Semestre", font=(FUENTE_APP, 16)
        ).pack()

        # entrada de texto para el nombre
        self.entry_nombre = ctk.CTkEntry(
            self.container, placeholder_text="Tu nombre aquí...", width=300, height=40
        )
        self.entry_nombre.pack(pady=20)

        # permite que la app funcione con la tecla enter
        self.entry_nombre.bind("<Return>", self.procesar_inicio)

        # boton de continuar
        ctk.CTkButton(
            self.container, text="Continuar", command=self.procesar_inicio, height=40
        ).pack(pady=10)

    # procesa el nombre ingresado por el usuario para iniciar el juego
    def procesar_inicio(self, event=None):
        nombre = self.entry_nombre.get().strip()
        if nombre:
            self.nombre_jugador = nombre
            self.seleccionar_categoria(self.nombre_jugador)

        # esto se imprimirá en la terminal de fondo
        print(f"[DEBUG] Botón presionado. Nombre capturado: '{nombre}'")

        # si el nombre no esta vacio, se inicia el juego
        if nombre:
            print("[DEBUG] Nombre válido. Cambiando a pantalla de categorías...")
            self.nombre_jugador = nombre
            self.seleccionar_categoria(nombre)
        else:
            # si el nombre esta vacio, se muestra un mensaje de error
            print("[DEBUG] El nombre estaba vacío.")
            self.entry_nombre.configure(
                placeholder_text="¡Por favor, escribe tu nombre!",
                placeholder_text_color="#ff6b6b",
            )

    # pantalla de seleccion de categoria
    def seleccionar_categoria(self, nombre):
        self.limpiar_pantalla()

        # titulo de la pantalla de seleccion de categoria
        ctk.CTkLabel(
            self.container,
            text=f"Hola {nombre}, elige una categoría:",
            font=(FUENTE_APP, 20),
        ).pack(pady=20)

        # lista de categorias
        categorias = [
            ("Países", "paises"),
            ("Animales", "animales"),
            ("Alimentos", "alimentos"),
            ("Películas", "peliculas"),
        ]

        # crea un boton por cada categoria
        for texto, valor in categorias:
            ctk.CTkButton(
                self.container,
                text=texto,
                width=200,
                command=lambda v=valor: self.callback_inicio(v),
            ).pack(pady=5)

    # pantalla de juego
    def mostrar_escenario(self, progreso, intentos, usadas):
        self.limpiar_pantalla()

        # layout de juego: Izquierda (Dibujo/Info) - Derecha (Palabra/Input)
        main_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # nombre del jugador en la parte pantalla
        ctk.CTkLabel(
            main_frame,
            text=f"Jugador: {self.nombre_jugador}",
            font=(FUENTE_APP, 16, "italic"),
            text_color="gray",
        ).pack(pady=(0, 10))

        # seccion de palabra (usamos la constante de fuente monoespaciada)
        if isinstance(progreso, list):
            texto_progreso = " ".join(progreso)
        else:
            texto_progreso = progreso

        # ajusta el tamaño de la fuente segun la longitud de la palabra
        tamanio_fuente = 45 if len(texto_progreso) < 20 else 28

        # palabra se ajusta al tamaño de la pantalla
        self.lbl_palabra = ctk.CTkLabel(
            main_frame,
            text=texto_progreso,
            font=(FUENTE_MONO, tamanio_fuente, "bold"),
            wraplength=700,
            justify="center",
        )
        self.lbl_palabra.pack(pady=40)

        # info de intentos
        self.lbl_info = ctk.CTkLabel(
            main_frame,
            text=f"Intentos: {intentos} | Usadas: {', '.join(usadas)}",
            font=(FUENTE_APP, 14),
        )
        self.lbl_info.pack(pady=10)

        # manejo de la entrada de letras
        self.input_letra = ctk.CTkEntry(
            main_frame,
            width=60,
            placeholder_text="A",
            font=(FUENTE_APP, 20),
            justify="center",
        )
        # permite que la app funcione con click o con la tecla enter
        self.input_letra.pack(pady=10)
        self.input_letra.bind("<Return>", lambda event: self.enviar_letra())

        # boton de adivinar
        ctk.CTkButton(main_frame, text="Adivinar", command=self.enviar_letra).pack(
            pady=10
        )
         # boton de pista 
        self.btn_pista = ctk.CTkButton(
            main_frame,
            text="💡 Obtener Pista (-1 vida)",
            command=self.callback_pista,
            fg_color="#3498db",  # Color principal (Azulcyan)
            hover_color="#2980b9",  # Color al pasar el mouse (Azul más oscuro)
        )
        self.btn_pista.pack(pady=20)

        # Protección al jugador: Desactiva la pista si el jugador moriría al usarla
        if intentos <= 1:
            self.btn_pista.configure(state="disabled")

    # envia la letra al motor del juego
    def enviar_letra(self):
        letra = self.input_letra.get().upper()
        self.input_letra.delete(0, "end")

        # validar si la letra es valida
        if len(letra) == 1 and letra.isalpha():
            self.callback_adivinar(letra)

    # pantalla de resultados
    def mostrar_resultado(self, gano, palabra_secreta):
        self.limpiar_pantalla()
        color = "#28a745" if gano else "#dc3545"
        texto = "¡VICTORIA!" if gano else "GAME OVER"

        # titulo de la pantalla de resultados
        ctk.CTkLabel(
            self.container, text=texto, font=(FUENTE_APP, 40, "bold"), text_color=color
        ).pack(pady=30)

        # palabra secreta
        ctk.CTkLabel(
            self.container,
            text=f"La palabra era: {palabra_secreta}",
            font=(FUENTE_APP, 18),
        ).pack(pady=10)

        # boton de jugar de nuevo
        ctk.CTkButton(
            self.container, text="Jugar de nuevo", command=self.reintentar_juego
        ).pack(pady=20)

    # permite que el usuario vuelva a jugar
    def reintentar_juego(self):
        if self.nombre_jugador:
            self.seleccionar_categoria(self.nombre_jugador)
        else:
            self.setup_pantalla_inicio()
