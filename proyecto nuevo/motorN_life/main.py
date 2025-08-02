import time
import json
from motor.nodos import crear_nodo, actualizar_nodo
from motor.campo import CampoInformacional
from motor.reglas import aplicar_reglas
from interfaz.canvas_campo import VisualizadorCampo

with open("datos/config.json", "r") as f:
    config = json.load(f)

campo = CampoInformacional(config)

for _ in range(10):
    nodo = crear_nodo(campo)
    campo.agregar_nodo(nodo)

ciclo = 0

def ciclo_motor():
    global ciclo
    for nodo in campo.nodos:
        actualizar_nodo(nodo, campo, config)
    aplicar_reglas(campo, config)
    ciclo += 1
    visual.root.after(config.get("ciclo_delay_ms", 300), ciclo_motor)

visual = VisualizadorCampo(campo)
visual.root.after(100, ciclo_motor)
visual.iniciar()