
import tkinter as tk
import numpy as np
from scipy.signal import convolve2d

import numpy as np
from scipy.signal import convolve2d

class MotorNDIGExtendido:
    def __init__(self, dim=50, gamma=0.1, lambda_=0.05, mu=0.5, kappa=0.3):
        """Inicializa el motor extendido con memoria persistente.
        
        Args:
            dim: Dimensión de la cuadrícula
            gamma: Coeficiente de difusión
            lambda_: Coeficiente de entropía
            mu: Tasa de actualización de la memoria (aumentado para mejor efecto)
            kappa: Fuerza de retroalimentación de la memoria (aumentado para mejor efecto)
        """
        self.dim = dim
        self.gamma = gamma
        self.lambda_ = lambda_
        self.mu = mu
        self.kappa = kappa
        
        # Campo principal
        self.rho = np.random.rand(dim, dim) * 0.1
        
        # Memoria persistente
        self.rho_mem = np.zeros((dim, dim))
        
        self.tiempo = 0

    def laplaciano(self, campo):
        return (
            -4 * campo
            + np.roll(campo, 1, axis=0)
            + np.roll(campo, -1, axis=0)
            + np.roll(campo, 1, axis=1)
            + np.roll(campo, -1, axis=1)
        )

    def entropia_local(self, campo):
        kernel = np.ones((3, 3)) / 9
        mean = convolve2d(campo, kernel, mode="same", boundary="wrap")
        varianza = convolve2d((campo - mean) ** 2, kernel, mode="same", boundary="wrap")
        return np.sqrt(varianza)

    def evolucionar(self):
        # Términos de evolución extendidos con memoria
        difusion = self.gamma * self.laplaciano(self.rho)
        entropia = self.lambda_ * self.entropia_local(self.rho)
        
        # Retroalimentación de la memoria (DIG effect)
        feedback_memoria = self.kappa * (self.rho_mem - self.rho)
        
        # Actualización del campo principal
        self.rho += difusion - entropia + feedback_memoria
        self.rho = np.clip(self.rho, 0, 1)
        
        # Actualización de la memoria (persistente)
        self.rho_mem += self.mu * (self.rho - self.rho_mem)
        
        self.tiempo += 1

    def reiniciar(self, reiniciar_memoria=False):
        """Reinicia el campo a un estado aleatorio inicial
        
        Args:
            reiniciar_memoria: Si es True, también reinicia la memoria persistente
        """
        self.rho = np.random.rand(self.dim, self.dim) * 0.1
        if reiniciar_memoria:
            self.rho_mem = np.zeros((self.dim, self.dim))
        self.tiempo = 0

    def inyectar(self, x, y, intensidad=1.0):
        """Inyecta información en una posición del campo y su memoria
        
        Args:
            x, y: Coordenadas donde inyectar
            intensidad: Cantidad a inyectar (ahora afecta tanto al campo como a la memoria)
        """
        try:
            if np.all((x >= 0) & (x < self.dim) & (y >= 0) & (y < self.dim)):
                # Inyectamos en el campo actual
                self.rho[y, x] = np.minimum(1.0, self.rho[y, x] + intensidad)
                # También actualizamos la memoria para reforzar el patrón
                self.rho_mem[y, x] = np.minimum(1.0, self.rho_mem[y, x] + intensidad * 0.5)
        except (ValueError, TypeError):
            # Fallback para cuando x o y no son arrays (el caso original)
            if 0 <= x < self.dim and 0 <= y < self.dim:
                self.rho[y, x] = min(1.0, self.rho[y, x] + intensidad)
                self.rho_mem[y, x] = min(1.0, self.rho_mem[y, x] + intensidad * 0.5)

    def obtener_rho(self):
        return self.rho

    def obtener_entropia_global(self):
        return np.mean(self.entropia_local(self.rho))

class MotorNApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Motor N - DIG Extendido")

        self.canvas = tk.Canvas(master, width=500, height=500, bg="black")
        self.canvas.pack()

        self.motor = MotorNDIGExtendido(dim=100, gamma=0.1, lambda_=0.05, mu=0.1, kappa=0.08)
        self.pixel_size = 5

        self.canvas.bind("<Button-1>", self.inyectar_click)
        self.actualizar()

    def inyectar_click(self, event):
        x = event.x // self.pixel_size
        y = event.y // self.pixel_size
        self.motor.inyectar(x, y, intensidad=1.0)  # Changed 'cantidad' to 'intensidad'

    def actualizar(self):
        self.motor.evolucionar()
        self.dibujar_campo()
        self.master.after(50, self.actualizar)

    def dibujar_campo(self):
        self.canvas.delete("all")
        for i in range(self.motor.dim):
            for j in range(self.motor.dim):
                valor = self.motor.rho[i, j]
                color = self.valor_a_color(valor)
                x1 = j * self.pixel_size
                y1 = i * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def valor_a_color(self, valor):
        tono = int(valor * 255)
        return f"#{tono:02x}{tono:02x}{tono:02x}"

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorNApp(root)
    root.mainloop()
