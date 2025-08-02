
import networkx as nx

class CID:
    def __init__(self):
        self.grafo = nx.Graph()

    def agregar_nodo(self, id, relevancia=1.0):
        self.grafo.add_node(id, relevancia=relevancia)

    def agregar_relacion(self, origen, destino):
        self.grafo.add_edge(origen, destino)

    def obtener_grafo(self):
        return self.grafo
