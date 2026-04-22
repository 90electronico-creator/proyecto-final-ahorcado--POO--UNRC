import sys
import random
from src.interfaz import Interfaz
from src.gestor_datos import GestorDatos
from src.palabra import Palabra
from src.jugador import Jugador


class MotorJuego:
    def __init__(self):
        # conectamos las funciones del motor con la interfaz visual
        self.interfaz = Interfaz(
            callback_adivinar=self.intentar_letra, callback_inicio=self.iniciar_partida, callback_pista=self.entregar_pista,
        )
        self.gestor = GestorDatos()
        self.jugador = None
        self.palabra_obj = None

    # inicia una nueva partida
    def iniciar_partida(self, categoria_id):
        nombre = getattr(self.interfaz, "nombre_jugador", "Jugador")
        self.jugador = Jugador(nombre)

        # carga las palabras de la categoría seleccionada
        lista_palabras = self.gestor.cargar_palabras(categoria_id)
        if not lista_palabras:
            print("❌ Error fatal: No hay palabras disponibles.")
            sys.exit()

        # selecciona una palabra al azar
        seleccion = random.choice(lista_palabras)
        self.palabra_obj = Palabra(seleccion)

        # actualiza la pantalla con la palabra seleccionada
        self.actualizar_pantalla()

    # intenta adivinar una letra
    def intentar_letra(self, letra):

        # verifica si la letra es correcta
        if not self.palabra_obj.verificar_letra(letra):
            if letra not in self.jugador.letras_usadas:
                self.jugador.descontar_vida()

       # registra el intento
        self.jugador.registrar_intento(letra)

        self.verificar_estado_juego()  

    # Lógica para revelar una letra a cambio de una vida 
    def entregar_pista(self):
        # Obtenemos las letras únicas de la palabra secreta (ignorando espacios)
        letras_secretas = set(self.palabra_obj.secreta.replace(" ", ""))

        # Obtenemos las letras que ya se descubrieron
        letras_descubiertas = set(self.palabra_obj.letras_adivinadas)

        # La resta de conjuntos nos da las letras que faltan por adivinar
        faltantes = list(letras_secretas - letras_descubiertas)

        # Verificamos que falten letras y que tenga vidas suficientes para la pista
        if faltantes and self.jugador.intentos_restantes > 1:
            # Elegimos una letra al azar de las que faltan
            letra_pista = random.choice(faltantes)

            # Cobramos la vida, revelamos la letra y la registramos
            self.jugador.descontar_vida()
            self.palabra_obj.verificar_letra(letra_pista)
            self.jugador.registrar_intento(letra_pista)

            # Reevaluamos si ganó o perdió con esta nueva letra revelada
            self.verificar_estado_juego()

    # --- Fin de la funcion de pista --

        # Valida si ganó o perdió
        if not self.jugador.tiene_vidas() or self.palabra_obj.es_palabra_completa():
            self.interfaz.mostrar_resultado(
                gano=self.palabra_obj.es_palabra_completa(),
                palabra_secreta=self.palabra_obj.secreta,
            )
        else:
            self.actualizar_pantalla()

    # actualiza la pantalla con la palabra seleccionada
    def actualizar_pantalla(self):
        self.interfaz.mostrar_escenario(
            progreso=self.palabra_obj.obtener_progreso(),
            intentos=self.jugador.intentos_restantes,
            usadas=self.jugador.letras_usadas,
        )


if __name__ == "__main__":
    app = MotorJuego()

    # inicia el bucle principal
    app.interfaz.mainloop()
