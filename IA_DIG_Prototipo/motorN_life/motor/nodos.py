import random

contador_nodos = 0

def crear_nodo(campo):
    global contador_nodos
    nodo = {
        "id": contador_nodos,
        "x": random.uniform(50, 450),
        "y": random.uniform(50, 450),
        "rho": random.uniform(0.5, 1.5),
        "kappa": random.uniform(-1.0, 1.0),
        "estado": "vivo",
        "edad": 0,
        "vecinos": []
    }
    contador_nodos += 1
    return nodo

def actualizar_nodo(nodo, campo, config, ciclo):
    if nodo["estado"] != "vivo":
        return

    nodo["edad"] += 1
    nodo["rho"] += random.uniform(-0.1, 0.1)
    nodo["rho"] = max(0, nodo["rho"])
    nodo["kappa"] += random.uniform(-0.05, 0.05)

    nodo["x"] += random.uniform(-1, 1)
    nodo["y"] += random.uniform(-1, 1)
    nodo["x"] = max(0, min(500, nodo["x"]))
    nodo["y"] = max(0, min(500, nodo["y"]))

    if nodo["rho"] < config["theta_death"] or abs(nodo["kappa"]) > config["delta_max"]:
        nodo["estado"] = "degradado"

    if nodo["rho"] > config["theta_colapso"] and abs(nodo["kappa"]) < config["delta_colapso"]:
        nodo["estado"] = "colapsado"
        campo.registrar_colapso(nodo, ciclo)