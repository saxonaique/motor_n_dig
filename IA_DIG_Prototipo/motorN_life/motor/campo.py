import math
import json
import os
from datetime import datetime

class CampoInformacional:
    def __init__(self, config):
        self.config = config
        self.nodos = []
        self.colapsos = 0
        self.log_colapsos = [] # Nueva lista para almacenar los colapsos

    def agregar_nodo(self, nodo):
        self.nodos.append(nodo)

    def obtener_vecinos(self, nodo, radio=50):
        vecinos = []
        for otro in self.nodos:
            if otro["id"] != nodo["id"] and otro["estado"] == "vivo":
                dx = nodo["x"] - otro["x"]
                dy = nodo["y"] - otro["y"]
                distancia = math.sqrt(dx**2 + dy**2)
                if distancia <= radio:
                    vecinos.append(otro)
        return vecinos

    def contar_por_estado(self):
        resumen = {"vivo": 0, "degradado": 0, "colapsado": 0}
        for nodo in self.nodos:
            resumen[nodo["estado"]] += 1
        return resumen

    def densidad_promedio(self):
        vivos = [n for n in self.nodos if n["estado"] == "vivo"]
        if not vivos:
            return 0
        return sum(n["rho"] for n in vivos) / len(vivos)

    def curvatura_promedio(self):
        vivos = [n for n in self.nodos if n["estado"] == "vivo"]
        if not vivos:
            return 0
        return sum(abs(n["kappa"]) for n in vivos) / len(vivos)

    def registrar_colapso(self, nodo, ciclo):
        self.colapsos += 1
        # Guardar una copia del nodo y el ciclo en el log
        self.log_colapsos.append({
            "ciclo": ciclo,
            "nodo_id": nodo["id"],
            "x": nodo["x"],
            "y": nodo["y"],
            "rho": nodo["rho"],
            "kappa": nodo["kappa"],
            "edad": nodo["edad"]
        })

    def guardar_log_colapsos(self):
        # Crear un nombre de archivo único con la fecha y hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Asegurarse de que el directorio 'logs' exista
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "logs")
        os.makedirs(log_dir, exist_ok=True)
        file_path = os.path.join(log_dir, f"colapsos_{timestamp}.json")
        
        with open(file_path, "w") as f:
            json.dump(self.log_colapsos, f, indent=4)
        print(f"Log de colapsos guardado en: {file_path}")
