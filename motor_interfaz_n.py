import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk
from motor_n_dig import MotorN

class MotorNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Motor N – Campo Informacional DIG")
        self.root.configure(bg="#111")
        
        self.canvas_size = 400
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="black", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.control_frame = ttk.Frame(root)
        self.control_frame.pack()

        ttk.Button(self.control_frame, text="Evolucionar", command=self.evolucionar).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Reiniciar", command=self.reiniciar).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.control_frame, text="Entropía:").grid(row=1, column=0)
        self.entropia_label = ttk.Label(self.control_frame, text="0.000")
        self.entropia_label.grid(row=1, column=1)

        self.canvas.bind("<Button-1>", self.inyectar)

        self.motor = MotorN(dim=50)
        self.actualizar_vista()

    def evolucionar(self):
        self.motor.evolucionar()
        self.actualizar_vista()

    def reiniciar(self):
        self.motor.reiniciar()
        self.actualizar_vista()

    def inyectar(self, event):
        x = int(event.x / self.canvas_size * self.motor.dim)
        y = int(event.y / self.canvas_size * self.motor.dim)
        self.motor.inyectar(x, y, intensidad=1.0)
        self.actualizar_vista()

    def actualizar_vista(self):
        campo = self.motor.obtener_rho()
        escala = (campo * 255).astype(np.uint8)
        imagen = Image.fromarray(escala).resize((self.canvas_size, self.canvas_size), Image.NEAREST)
        self.tk_image = ImageTk.PhotoImage(imagen.convert("L"))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        entropia = self.motor.obtener_entropia_global()
        self.entropia_label.config(text=f"{entropia:.3f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorNApp(root)
    root.mainloop()


class MotorNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Motor N – Campo Informacional DIG")
        self.root.configure(bg="#111")
        
        self.canvas_size = 400
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="black", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.control_frame = ttk.Frame(root)
        self.control_frame.pack()

        ttk.Button(self.control_frame, text="Evolucionar", command=self.evolucionar).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Reiniciar", command=self.reiniciar).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.control_frame, text="Entropía:").grid(row=1, column=0)
        self.entropia_label = ttk.Label(self.control_frame, text="0.000")
        self.entropia_label.grid(row=1, column=1)

        self.canvas.bind("<Button-1>", self.inyectar)

        self.motor = MotorN(dim=50)
        self.actualizar_vista()

    def evolucionar(self):
        self.motor.evolucionar()
        self.actualizar_vista()

    def reiniciar(self):
        self.motor.reiniciar()
        self.actualizar_vista()

    def inyectar(self, event):
        x = int(event.x / self.canvas_size * self.motor.dim)
        y = int(event.y / self.canvas_size * self.motor.dim)
        self.motor.inyectar(x, y, intensidad=1.0)
        self.actualizar_vista()

    def actualizar_vista(self):
        campo = self.motor.obtener_rho()
        escala = (campo * 255).astype(np.uint8)
        imagen = Image.fromarray(escala).resize((self.canvas_size, self.canvas_size), Image.NEAREST)
        self.tk_image = ImageTk.PhotoImage(imagen.convert("L"))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        entropia = self.motor.obtener_entropia_global()
        self.entropia_label.config(text=f"{entropia:.3f}")


from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk
from motor_n_dig import MotorN

class MotorNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Motor N – Campo Informacional DIG")
        self.root.configure(bg="#111")
        
        self.canvas_size = 400
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="black", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.control_frame = ttk.Frame(root)
        self.control_frame.pack()

        ttk.Button(self.control_frame, text="Evolucionar", command=self.evolucionar).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Reiniciar", command=self.reiniciar).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.control_frame, text="Entropía:").grid(row=1, column=0)
        self.entropia_label = ttk.Label(self.control_frame, text="0.000")
        self.entropia_label.grid(row=1, column=1)

        self.canvas.bind("<Button-1>", self.inyectar)

        self.motor = MotorN(dim=50)
        self.actualizar_vista()

    def evolucionar(self):
        self.motor.evolucionar()
        self.actualizar_vista()

    def reiniciar(self):
        self.motor.reiniciar()
        self.actualizar_vista()

    def inyectar(self, event):
        x = int(event.x / self.canvas_size * self.motor.dim)
        y = int(event.y / self.canvas_size * self.motor.dim)
        self.motor.inyectar(x, y, intensidad=1.0)
        self.actualizar_vista()

    def actualizar_vista(self):
        campo = self.motor.obtener_rho()
        escala = (campo * 255).astype(np.uint8)
        imagen = Image.fromarray(escala).resize((self.canvas_size, self.canvas_size), Image.NEAREST)
        self.tk_image = ImageTk.PhotoImage(imagen.convert("L"))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        entropia = self.motor.obtener_entropia_global()
if __name__ == "__main__":
    root = tk.Tk()
    app = MotorNApp(root)
    root.mainloop()
