
class NCD:
    def __init__(self, cid, delta=0.5, theta=4.0):
        self.cid = cid
        self.delta = delta
        self.theta = theta
        self.colapsados = []

    def detectar_colapso(self):
        for nodo in self.cid.grafo.nodes:
            rho = self.cid.grafo.nodes[nodo].get("rho", 0.0)
            kappa = self.cid.grafo.nodes[nodo].get("curvatura", 0.0)
            if abs(kappa) < self.delta and rho > self.theta:
                self.cid.grafo.nodes[nodo]["colapsado"] = True
                self.colapsados.append(nodo)
            else:
                self.cid.grafo.nodes[nodo]["colapsado"] = False
        return self.colapsados
