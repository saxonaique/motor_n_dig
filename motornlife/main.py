import time
import json
import os
import sys
import threading

# Agregar el directorio raíz del proyecto a la ruta de búsqueda de módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .motor.nodos import crear_nodo, actualizar_nodo
from .motor.campo import CampoInformacional
from .motor.reglas import aplicar_reglas
from motor_interfaz_n import MotorNApp
import tkinter as tk

# Cargar configuración
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "datos", "config.json")
with open(config_path, "r") as f:
    config = json.load(f)

# Inicializar el campo informacional
campo = CampoInformacional(config)

# Iniciar visualización
root = tk.Tk()
app = MotorNApp(root)


# Generar nodos iniciales (10 por ahora)
for _ in range(10):
    nodo = crear_nodo(campo)
    campo.agregar_nodo(nodo)

# Ciclo de simulación
ciclo = 0
try:
    while True:
        print(f"\n🔁 Ciclo {ciclo}")
        for nodo in campo.nodos:
            actualizar_nodo(nodo, campo, config)
            print(f"🧠 Nodo {nodo['id']} → estado: {nodo['estado']}, ρ: {nodo['rho']:.2f}, κ: {nodo['kappa']:.2f}, edad: {nodo['edad']}")

        aplicar_reglas(campo, config)

        ciclo += 1
        time.sleep(config.get("ciclo_delay_ms", 200) / 1000)

except KeyboardInterrupt:
    print("\n🛑 Simulación detenida manualmente.")