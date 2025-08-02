import math

class CampoInformacional:
    def __init__(self, config):
        self.config = config
        self.nodos = []
        self.colapsos = 0

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

    def registrar_colapso(self):
        self.colapsos += 1