import time
import json
import os
from motor.nodos import crear_nodo, actualizar_nodo
from motor.campo import CampoInformacional
from motor.reglas import aplicar_reglas
from interfaz.canvas_campo import VisualizadorCampo

# Construir la ruta absoluta al archivo de configuración
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "datos", "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

ciclo = 0 # Inicializamos la variable ciclo

def ciclo_motor(campo, visual, config):
    """Función principal del ciclo del motor."""
    global ciclo # Declaramos ciclo como global
    for nodo in campo.nodos:
        actualizar_nodo(nodo, campo, config)
    aplicar_reglas(campo, config)
    visual.root.after(config.get("ciclo_delay_ms", 300), lambda: ciclo_motor(campo, visual, config))
    
    ciclo += 1

def main():
    """Función principal para configurar y ejecutar la simulación."""
    campo = CampoInformacional(config)

    for _ in range(10):
        nodo = crear_nodo(campo)
        campo.agregar_nodo(nodo)

    visual = VisualizadorCampo(campo)
    
    # Pasamos los objetos necesarios a la función del ciclo
    visual.root.after(100, lambda: ciclo_motor(campo, visual, config))
    visual.iniciar()

if __name__ == "__main__":
    main()
