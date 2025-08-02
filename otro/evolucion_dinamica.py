
import random
import time

class EvolucionCID:
    def __init__(self, cid, mgi, ncd, visualizador, ciclos=5, delay=2.0):
        self.cid = cid
        self.mgi = mgi
        self.ncd = ncd
        self.visualizador = visualizador
        self.ciclos = ciclos
        self.delay = delay
        self.contador = 0

    def ciclo(self):
        nuevo_nodo = f"N{self.contador}"
        relevancia = round(random.uniform(0.5, 3.5), 2)
        self.cid.agregar_nodo(nuevo_nodo, relevancia=relevancia)

        if self.cid.grafo.number_of_nodes() > 1:
            vecinos = random.sample(list(self.cid.grafo.nodes), k=min(2, self.cid.grafo.number_of_nodes()))
            for v in vecinos:
                if v != nuevo_nodo:
                    self.cid.agregar_relacion(nuevo_nodo, v)

        self.mgi.aplicar_gravedad_y_curvatura()
        self.ncd.detectar_colapso()

        # Visualizaciones
        self.visualizador.mostrar_valor(self.cid.grafo, "rho", f"Ciclo {self.contador}: Densidad ρ(u)")
        self.visualizador.mostrar_valor(self.cid.grafo, "curvatura", f"Ciclo {self.contador}: Curvatura κ(u)", cmap='coolwarm')
        self.visualizador.mostrar_valor(self.cid.grafo, "tiempo", f"Ciclo {self.contador}: Tiempo τ(u)", cmap='plasma')
        self.visualizador.mostrar_colapso(self.cid.grafo)

        self.contador += 1

    def ejecutar(self):
        for _ in range(self.ciclos):
            self.ciclo()
            time.sleep(self.delay)
