# clase palabra
class Palabra:
    # inicializa la palabra
    def __init__(self, texto_secreto):
        self.secreta = texto_secreto.upper()
        self.letras_adivinadas = []

    # verifica si la letra es correcta
    def verificar_letra(self, letra):
        letra = letra.upper()
        if letra in self.secreta:
            if letra not in self.letras_adivinadas:
                self.letras_adivinadas.append(letra)
            return True
        return False

    # devuelve algo como "A _ _ O _"
    def obtener_progreso(self):
        return " ".join(
            [l if l in self.letras_adivinadas else "_" for l in self.secreta]
        )

    # verifica si la palabra esta completa
    def es_palabra_completa(self):
        return all(l in self.letras_adivinadas for l in self.secreta)
