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
        self.root.geometry("800x800")
        self.root.minsize(600, 600)
        self.root.resizable(True, True)

        self.canvas_size = 700
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="black", highlightthickness=0)
        self.canvas.pack(pady=10, expand=True)

        self.control_frame = ttk.Frame(root)
        self.control_frame.pack(fill=tk.X, pady=10)

        ttk.Button(self.control_frame, text="Evolucionar", command=self.evolucionar).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Reiniciar", command=self.reiniciar).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.control_frame, text="Entropía:").grid(row=1, column=0)
        self.entropia_label = ttk.Label(self.control_frame, text="0.000")
        self.entropia_label.grid(row=1, column=1)

        # Slider para velocidad de animación
        ttk.Label(self.control_frame, text="Velocidad (ms):").grid(row=2, column=0)
        self.velocidad = tk.IntVar(value=100)
        self.slider = ttk.Scale(self.control_frame, from_=10, to=1000, variable=self.velocidad, orient=tk.HORIZONTAL)
        self.slider.grid(row=2, column=1, sticky="ew", padx=5)
        self.control_frame.columnconfigure(1, weight=1)

        # Botón de animación
        self.animando = False
        self.boton_animar = ttk.Button(self.control_frame, text="Iniciar animación", command=self.toggle_animacion)
        self.boton_animar.grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Guardar campo", command=self.guardar_campo).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Cargar campo", command=self.cargar_campo).grid(row=0, column=4, padx=5, pady=5)

        self.canvas.bind("<Button-1>", self.inyectar)
        self.canvas.bind("<B1-Motion>", self.pintar_lapiz)

        self.motor = MotorN(dim=100)
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

    def pintar_lapiz(self, event):
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

    def toggle_animacion(self):
        self.animando = not self.animando
        if self.animando:
            self.boton_animar.config(text="Pausar animación")
            self.animar()
        else:
            self.boton_animar.config(text="Iniciar animación")

    def animar(self):
        if self.animando:
            self.evolucionar()
            self.root.after(self.velocidad.get(), self.animar)

    def guardar_campo(self):
        import os
        import datetime
        carpeta = os.path.join(os.path.dirname(__file__), "datos_campo")
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = os.path.join(carpeta, f"campo_{fecha}.npy")
        np.save(ruta, self.motor.obtener_rho())
        print(f"Campo guardado en {ruta}")

    def cargar_campo(self):
        import os
        from tkinter import filedialog, messagebox
        carpeta = os.path.join(os.path.dirname(__file__), "datos_campo")
        archivo = filedialog.askopenfilename(initialdir=carpeta, title="Selecciona archivo de campo",
                                             filetypes=[("NumPy files", "*.npy")])
        if archivo:
            try:
                datos = np.load(archivo)
                if datos.shape == self.motor.rho.shape:
                    self.motor.rho = datos
                    self.actualizar_vista()
                    print(f"Campo cargado de {archivo}")
                else:
                    messagebox.showerror("Error", f"Dimensiones incompatibles: {datos.shape}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorNApp(root)
    root.mainloop()






