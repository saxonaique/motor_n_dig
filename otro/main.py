from cid_grafo import CID
from mgi_gravedad import MGI
from ncd_colapso import NCD

# Crear campo
cid = CID()
cid.agregar_nodo("A", relevancia=1.0)
cid.agregar_nodo("B", relevancia=2.0)
cid.agregar_nodo("C", relevancia=3.5)
cid.agregar_nodo("D", relevancia=1.2)

cid.agregar_relacion("A", "B")
cid.agregar_relacion("B", "C")
cid.agregar_relacion("C", "D")
cid.agregar_relacion("A", "D")

# Gravedad y curvatura
mgi = MGI(cid)
mgi.aplicar_gravedad_y_curvatura()

# Colapso
ncd = NCD(cid, delta=0.5, theta=4.0)
nodos_colapsados = ncd.detectar_colapso()

# --- Conectar módulos principales a la interfaz gráfica ---
import tkinter as tk
from motor_interfaz_n import MotorNApp
import numpy as np

class GrafoAutomata:
    def __init__(self, nodo_id, relevancia, campo, x, y, color="blue"):
        self.nodo_id = nodo_id
        self.relevancia = relevancia
        self.x = x  # Normalizado [0,1]
        self.y = y
        self.campo = campo  # Referencia al campo (matriz numpy)
        self.radio = 5
        self.draw_radio = 15  # Radio para el dibujado
        self.color = color
        self.vx = 0.0
        self.vy = 0.0

    def actualizar_estado(self, grafo, idx, nodos_pos, canvas_size, fuerza=0.01):
        # Movimiento por atracción/repulsión según relaciones y relevancia
        ax, ay = 0.0, 0.0
        mi_pos = np.array([self.x, self.y])
        for j, (otro_id, otro_pos) in enumerate(nodos_pos.items()):
            if otro_id == self.nodo_id:
                continue
            
            otro_relevancia = grafo.nodes[otro_id].get("relevancia", 1.0)
            delta = np.array(otro_pos) - mi_pos
            dist = np.linalg.norm(delta) + 1e-6 # Evitar división por cero

            # Fuerza de atracción para nodos conectados (más fuerte)
            if grafo.has_edge(self.nodo_id, otro_id):
                fuerza_atraccion = 0.05 * np.log(dist / 0.5)
                ax += fuerza_atraccion * delta[0] / dist
                ay += fuerza_atraccion * delta[1] / dist
            
            # Fuerza de repulsión para todos los nodos (más débil)
            fuerza_repulsion = -0.001 * (self.relevancia * otro_relevancia) / (dist**2)
            ax += fuerza_repulsion * delta[0] / dist
            ay += fuerza_repulsion * delta[1] / dist

        # Actualiza velocidad y posición
        self.vx = 0.9 * self.vx + fuerza * ax
        self.vy = 0.9 * self.vy + fuerza * ay
        
        # Evita que los nodos se salgan del canvas
        margin = self.draw_radio / canvas_size
        self.x = np.clip(self.x + self.vx, margin, 1.0 - margin)
        self.y = np.clip(self.y + self.vy, margin, 1.0 - margin)

    def color_estado(self, grafo):
        # Cambia color según estado (colapsado, curvatura, etc)
        if grafo.nodes[self.nodo_id].get("colapsado", False):
            return "red"
        curv = grafo.nodes[self.nodo_id].get("curvatura", 0)
        if curv > 1.0:
            return "orange"
        elif curv < -1.0:
            return "cyan"
        else:
            return "lime"

    def draw(self, canvas, canvas_size, nodos_pos, grafo):
        cx = int(self.x * canvas_size)
        cy = int(self.y * canvas_size)
        r = self.draw_radio
        # Dibuja conexiones (aristas) desde este nodo a los conectados
        for otro_id, (ox, oy) in nodos_pos.items():
            if otro_id != self.nodo_id and grafo.has_edge(self.nodo_id, otro_id):
                ocx = int(ox * canvas_size)
                ocy = int(oy * canvas_size)
                canvas.create_line(cx, cy, ocx, ocy, fill="#888", width=2)
        # Dibuja el nodo/partícula
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=self.color, outline="black", width=2)
        canvas.create_text(cx, cy, text=str(self.nodo_id), fill="black", font=("Arial", 10, "bold"))

    def aplicar_al_campo(self, gamma=0.1):
        # El autómata modifica el campo en su posición según su relevancia y gamma
        dim = self.campo.shape[0]
        x0 = int(self.x * dim)
        y0 = int(self.y * dim)
        for i in range(max(0, x0-self.radio), min(dim, x0+self.radio+1)):
            for j in range(max(0, y0-self.radio), min(dim, y0+self.radio+1)):
                dist = ((i-x0)**2 + (j-y0)**2)**0.5
                if dist <= self.radio:
                    self.campo[i, j] += self.relevancia * gamma * (1 - dist/self.radio)
        np.clip(self.campo, 0, 1, out=self.campo)

class MotorNAppAdaptada(MotorNApp):
    def __init__(self, root, cid, mgi, ncd):
        self.cid = cid
        self.mgi = mgi
        self.ncd = ncd
        super().__init__(root)
        self.automatas = []
        self._crear_automatas_grafo()
        self._patch_canvas_draw()
        self.animando = True  # Animación continua por defecto
        self._animar_grafo()  # Inicia la animación al arrancar

    def _crear_automatas_grafo(self):
        # Distribuye los nodos del grafo sobre el campo como autómatas
        self.automatas.clear()
        for nodo, datos in self.cid.grafo.nodes(data=True):
            x = np.random.uniform(0.1, 0.9)
            y = np.random.uniform(0.1, 0.9)
            relevancia = datos.get("relevancia", 1.0)
            automata = GrafoAutomata(nodo, relevancia, self.motor.rho, x, y)
            self.automatas.append(automata)

    def evolucionar_grafo(self):
        # Aplica la evolución del grafo y de los autómatas sobre el campo
        self.mgi.aplicar_gravedad_y_curvatura()
        self.ncd.detectar_colapso()
        gamma = getattr(self.motor, "gamma", 0.1)
        # Actualiza posiciones de autómatas
        nodos_pos = {a.nodo_id: (a.x, a.y) for a in self.automatas}
        canvas_size = self.canvas_size  # Obtener el tamaño del lienzo
        for idx, automata in enumerate(self.automatas):
            automata.actualizar_estado(self.cid.grafo, idx, nodos_pos, canvas_size)
            automata.color = automata.color_estado(self.cid.grafo)
            automata.aplicar_al_campo(gamma=gamma)
        # Evoluciona el campo como autómata celular
        self.motor.evolucionar()
        # Si hay nuevos nodos en el grafo, añádelos como autómatas
        self._sincronizar_automatas_con_grafo()
        self.actualizar_vista()

    def _sincronizar_automatas_con_grafo(self):
        # Añade autómatas para nuevos nodos del grafo
        existentes = {a.nodo_id for a in self.automatas}
        nuevos = [n for n in self.cid.grafo.nodes if n not in existentes]
        if nuevos:
            for nodo in nuevos:
                datos = self.cid.grafo.nodes[nodo]
                x = np.random.uniform(0.1, 0.9)
                y = np.random.uniform(0.1, 0.9)
                relevancia = datos.get("relevancia", 1.0)
                automata = GrafoAutomata(nodo, relevancia, self.motor.rho, x, y)
                self.automatas.append(automata)

    def mostrar_metricas(self):
        # Calcula y muestra métricas del grafo y nodos en la interfaz
        import networkx as nx
        G = self.cid.grafo
        metricas = []
        metricas.append(f"Nodos: {G.number_of_nodes()}  Aristas: {G.number_of_edges()}")
        if G.number_of_nodes() > 0:
            grados = dict(G.degree())
            metricas.append(f"Grado medio: {np.mean(list(grados.values())):.2f}")
            metricas.append(f"Grado máx: {np.max(list(grados.values()))}, min: {np.min(list(grados.values()))}")
            clustering = nx.average_clustering(G)
            metricas.append(f"Clustering medio: {clustering:.2f}")
            try:
                if nx.is_connected(G.to_undirected()):
                    diam = nx.diameter(G.to_undirected())
                    metricas.append(f"Diámetro: {diam}")
            except Exception:
                pass
            # Métricas de nodos
            for n in G.nodes:
                curv = G.nodes[n].get("curvatura", 0)
                rho = G.nodes[n].get("rho", 0)
                colapsado = G.nodes[n].get("colapsado", False)
                metricas.append(f"Nodo {n}: grado={grados[n]}, curv={curv:.2f}, rho={rho:.2f}, colapsado={colapsado}")
        # Muestra en el área de texto de la interfaz
        if hasattr(self, "text_area"):
            self.text_area.config(state='normal')
            self.text_area.delete(1.0, "end")
            self.text_area.insert("end", "\n".join(metricas))
            self.text_area.config(state='disabled')

    def evolucionar(self):
        # Al pulsar el botón "Evolucionar", añade un nodo nuevo y evoluciona el grafo/campo
        self.anadir_nodo_grafo()
        self.evolucionar_grafo()
        self.mostrar_metricas()

    def _patch_canvas_draw(self):
        # Sobrescribe el método actualizar_vista para dibujar partículas y conexiones
        original_actualizar_vista = self.actualizar_vista
        def nueva_actualizar_vista():
            original_actualizar_vista()
            canvas = self.canvas
            canvas_size = self.canvas_size
            nodos_pos = {a.nodo_id: (a.x, a.y) for a in self.automatas}
            # Dibuja conexiones y partículas
            for automata in self.automatas:
                automata.draw(canvas, canvas_size, nodos_pos, self.cid.grafo)
        self.actualizar_vista = nueva_actualizar_vista

    def toggle_animacion(self):
        # Ahora solo pausa/reanuda la animación continua
        self.animando = not self.animando
        if self.animando:
            self.boton_animar.config(text="Pausar animación")
            self._animar_grafo()
        else:
            self.boton_animar.config(text="Iniciar animación")

    def _animar_grafo(self):
        if self.animando:
            self.evolucionar_grafo()
            self.mostrar_metricas()
            self.root.after(self.velocidad.get(), self._animar_grafo)

    def anadir_nodo_grafo(self, relevancia=None):
        # Método para añadir un nodo nuevo al grafo y como autómata
        import random
        nuevo_id = f"N{len(self.cid.grafo.nodes)+1}"
        if relevancia is None:
            relevancia = random.uniform(1.0, 4.0)
        self.cid.agregar_nodo(nuevo_id, relevancia=relevancia)
        # Conectar a un nodo existente aleatorio
        if len(self.cid.grafo.nodes) > 1:
            destino = random.choice(list(self.cid.grafo.nodes))
            while destino == nuevo_id and len(self.cid.grafo.nodes) > 1:
                destino = random.choice(list(self.cid.grafo.nodes))
            self.cid.agregar_relacion(nuevo_id, destino)
        self._sincronizar_automatas_con_grafo()
        self.actualizar_vista()

    # Puedes añadir un botón en la interfaz para llamar a anadir_nodo_grafo si lo deseas

# Lanzar la interfaz adaptada
if __name__ == "__main__":
    root = tk.Tk()
    app = MotorNAppAdaptada(root, cid, mgi, ncd)
    root.mainloop()

# --- Otras interfaces y visualizaciones desactivadas ---
# from motor_visual import MotorNVisual
# MotorNVisual(cid, mgi, ncd).iniciar()
# from interfaz_grafica import InterfazGraficaCID
# InterfazGraficaCID(cid, mgi, ncd).iniciar()
# from visualizador import mostrar_valor, mostrar_colapso
# mostrar_valor(cid.grafo, "rho", "Densidad Informacional ρ(u)")
# mostrar_valor(cid.grafo, "curvatura", "Curvatura Informacional κ(u)", cmap='coolwarm')
# mostrar_valor(cid.grafo, "tiempo", "Tiempo Emergente τ(u)", cmap='plasma')
# mostrar_colapso(cid.grafo)
# from evolucion_dinamica import EvolucionCID
# evo = EvolucionCID(cid, mgi, ncd, visualizador=__import__('visualizador'), ciclos=5, delay=1.5)
# evo.ejecutar()
# mostrar_colapso(cid.grafo)
# from evolucion_dinamica import EvolucionCID
# evo = EvolucionCID(cid, mgi, ncd, visualizador=__import__('visualizador'), ciclos=5, delay=1.5)
# evo.ejecutar()
