# clase que crea el jugador
class Jugador:
    # inicializa el jugador
    def __init__(self, nombre, intentos_maximos=6):
        self.nombre = nombre
        self.intentos_restantes = intentos_maximos
        self.letras_usadas = []

    # registra el intento del jugador
    def registrar_intento(self, letra):
        letra = letra.upper()
        if letra not in self.letras_usadas:
            self.letras_usadas.append(letra)

    # descuenta una vida al jugador
    def descontar_vida(self):
        self.intentos_restantes -= 1

    # verifica si el jugador tiene vidas
    def tiene_vidas(self):
        return self.intentos_restantes > 0
