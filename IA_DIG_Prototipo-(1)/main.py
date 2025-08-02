
from cid_grafo import CID
from mgi_gravedad import MGI
from ncd_colapso import NCD
from visualizador import mostrar_valor, mostrar_colapso

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

# Visualizaciones
mostrar_valor(cid.grafo, "rho", "Densidad Informacional ρ(u)")
mostrar_valor(cid.grafo, "curvatura", "Curvatura Informacional κ(u)", cmap='coolwarm')
mostrar_valor(cid.grafo, "tiempo", "Tiempo Emergente τ(u)", cmap='plasma')
mostrar_colapso(cid.grafo)


# --- Ejemplo de evolución dinámica (descomenta para probar) ---
# from evolucion_dinamica import EvolucionCID
# evo = EvolucionCID(cid, mgi, ncd, visualizador=__import__('visualizador'), ciclos=5, delay=1.5)
# evo.ejecutar()
