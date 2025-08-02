import tkinter as tk

class VisualizadorCampo:
    def __init__(self, campo):
        self.campo = campo
        self.root = tk.Tk()
        self.root.title("Motor N – Campo Informacional")
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="black")
        self.canvas.pack()
        self.root.after(100, self.actualizar)

    def dibujar_nodos(self):
        self.canvas.delete("all")
        for nodo in self.campo.nodos:
            x = nodo["x"]
            y = nodo["y"]
            estado = nodo["estado"]

            if estado == "colapsado":
                color = "lime"
                radio = 6
            elif estado == "degradado":
                color = "gray"
                radio = 2
            else:  # vivo
                color = "white"
                radio = 4

            self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill=color)

    def actualizar(self):
        self.dibujar_nodos()
        self.root.after(100, self.actualizar)

    def iniciar(self):
        self.root.mainloop()
if __name__ == '__main__':
    from motornlife.motor.campo import Campo
    campo = Campo()  # Crear una instancia de Campo
    visual = VisualizadorCampo(campo)
    visual.iniciar()
