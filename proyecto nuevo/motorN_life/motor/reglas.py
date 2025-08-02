from motor.nodos import crear_nodo

def aplicar_reglas(campo, config):
    nuevos_nodos = []

    for nodo in campo.nodos:
        if nodo["estado"] != "vivo":
            continue

        vecinos = campo.obtener_vecinos(nodo, radio=50)
        nodo["vecinos"] = [v["id"] for v in vecinos]
        promedio_rho = sum(v["rho"] for v in vecinos) / len(vecinos) if vecinos else 0

        if promedio_rho > config["theta_birth"] and len(vecinos) >= 2:
            nuevo = crear_nodo(campo)
            nuevo["x"] = nodo["x"] + 10
            nuevo["y"] = nodo["y"] + 10
            nuevos_nodos.append(nuevo)

    for nuevo in nuevos_nodos:
        campo.agregar_nodo(nuevo)