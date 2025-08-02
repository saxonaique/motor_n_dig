
class CampoInformacional:
    def __init__(self, config):
        self.config = config
        self.nodos = []

    def agregar_nodo(self, nodo):
        self.nodos.append(nodo)

    def obtener_vecinos(self, nodo, radio=50):
        vecinos = []
        for otro in self.nodos:
            if otro["id"] != nodo["id"] and otro["estado"] == "vivo":
                dx = nodo["posicion"][0] - otro["posicion"][0]
                dy = nodo["posicion"][1] - otro["posicion"][1]
                distancia = (dx**2 + dy**2)**0.5
                if distancia <= radio:
                    vecinos.append(otro)
        return vecinos
