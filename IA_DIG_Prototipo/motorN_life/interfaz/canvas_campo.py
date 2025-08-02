import tkinter as tk

class VisualizadorCampo:
    def __init__(self, campo):
        self.campo = campo
        self.root = tk.Tk()
        self.root.title("Motor N – Campo Informacional")
        self.canvas = tk.Canvas(self.root, width=500, height=520, bg="black") # Altura ajustada
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.agregar_nodo_click) # Enlazar clic
        self.root.after(100, self.actualizar)

    def agregar_nodo_click(self, event):
        # Asegurarse de que el ID sea único
        if self.campo.nodos:
            new_id = max([n["id"] for n in self.campo.nodos]) + 1
        else:
            new_id = 0

        nuevo = {
            "id": new_id,
            "x": event.x,
            "y": event.y,
            "rho": 1.0,
            "kappa": 0.0,
            "estado": "vivo",
            "edad": 0,
            "vecinos": []
        }
        self.campo.agregar_nodo(nuevo)

    def dibujar_nodos(self):
        self.canvas.delete("all")
        for nodo in self.campo.nodos:
            x = nodo["x"]
            y = nodo["y"]
            estado = nodo["estado"]

            if estado == "colapsado":
                color = "lime"
                radio = 6
                self.canvas.create_text(x, y - 10, text="★", fill="lime", font=("Helvetica", 8))
            elif estado == "degradado":
                color = "gray"
                radio = 2
            else:
                color = "white"
                radio = 4

            self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill=color)

        # HUD informacional
        resumen = self.campo.contar_por_estado()
        densidad = self.campo.densidad_promedio()
        curvatura = self.campo.curvatura_promedio()
        self.canvas.create_text(
            250, 505, fill="white", font=("Helvetica", 10),
            text=f"Vivos: {resumen['vivo']}  |  Colapsados: {resumen['colapsado']}  |  Densidad promedio: {densidad:.2f}  |  Curvatura promedio: {curvatura:.2f}"
        )

    def actualizar(self):
        self.dibujar_nodos()
        # Ya no actualizamos el título aquí, la información está en el HUD
        self.root.after(100, self.actualizar)

    def iniciar(self):
        self.root.mainloop()