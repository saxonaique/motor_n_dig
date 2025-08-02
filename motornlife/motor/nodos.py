import random

# Contador de nodos únicos (simple, mejorable si hay multihilos)
contador_nodos = 0

def crear_nodo(campo):
    global contador_nodos
    nodo = {
        "id": contador_nodos,
        "posicion": [random.uniform(50, 450), random.uniform(50, 450)],
        "rho": random.uniform(0.5, 1.5),  # Densidad informacional inicial
        "kappa": random.uniform(-1.0, 1.0),  # Curvatura (tensión)
        "estado": "vivo",
        "edad": 0,
        "vecinos": []
    }
    contador_nodos += 1
    return nodo

def actualizar_nodo(nodo, campo, config):
    if nodo["estado"] != "vivo":
        return  # No hacemos nada si ya está colapsado o degradado

    nodo["edad"] += 1

    # Simulación simple de variación interna
    nodo["rho"] += random.uniform(-0.1, 0.1)
    nodo["rho"] = max(0, nodo["rho"])  # No puede ser negativa

    nodo["kappa"] += random.uniform(-0.05, 0.05)

    # Aplicar condiciones de degradación (visual)
    if nodo["rho"] < config["theta_death"] or abs(nodo["kappa"]) > config["delta_max"]:
        nodo["estado"] = "degradado"

    # Colapso informacional (hipótesis emergente)
    if nodo["rho"] > config["theta_colapso"] and abs(nodo["kappa"]) < config["delta_colapso"]:
        nodo["estado"] = "colapsado"
