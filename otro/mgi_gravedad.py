
class MGI:
    def __init__(self, cid, alpha=1.0, beta=0.5):
        self.cid = cid
        self.alpha = alpha
        self.beta = beta

    def calcular_rho(self, nodo):
        grafo = self.cid.grafo
        R = grafo.nodes[nodo].get('relevancia', 1.0)
        C = grafo.degree(nodo)
        return self.alpha * R + self.beta * C

    def calcular_curvatura(self, nodo, rho_u):
        return sum(self.calcular_rho(v) - rho_u for v in self.cid.grafo.neighbors(nodo))

    def aplicar_gravedad_y_curvatura(self, gamma=2.0):
        for nodo in self.cid.grafo.nodes:
            rho_u = self.calcular_rho(nodo)
            self.cid.grafo.nodes[nodo]["rho"] = rho_u

        for nodo in self.cid.grafo.nodes:
            rho_u = self.cid.grafo.nodes[nodo]["rho"]
            kappa = self.calcular_curvatura(nodo, rho_u)
            self.cid.grafo.nodes[nodo]["curvatura"] = kappa
            self.cid.grafo.nodes[nodo]["tiempo"] = 1.0 + gamma * abs(kappa)

        for u, v in self.cid.grafo.edges:
            rho_u = self.cid.grafo.nodes[u]["rho"]
            rho_v = self.cid.grafo.nodes[v]["rho"]
            self.cid.grafo[u][v]["peso"] = rho_u * rho_v
