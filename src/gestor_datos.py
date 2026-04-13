import json
import os


# clase que se encarga de cargar las palabras desde un archivo json
class GestorDatos:
    @staticmethod
    def cargar_palabras(nombre_archivo):

        # lee un archivo json y devuelve la lista de palabras,además se manejan los errores si el archivo no existe o esta mal formado
        ruta = os.path.join("data", f"{nombre_archivo}.json")
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                return datos.get("palabras", [])
        except FileNotFoundError:
            # aqui lanzamos una alerta pero el programa no "explota"
            print(f"⚠️ Error: No se encontró el archivo en {ruta}")
            return []
            # si el archivo esta mal formado
        except json.JSONDecodeError:
            print(
                f"⚠️ Error: El archivo {nombre_archivo}.json tiene un formato inválido"
            )
            return []
