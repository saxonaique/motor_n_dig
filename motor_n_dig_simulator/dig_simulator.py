import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def simular_universo_dig(resolucion=200, rho_c=1.0, Rs=20.0, k_c2=1.0, delta_q=0.1):
    x = np.linspace(-Rs, Rs, resolucion)
    y = np.linspace(-Rs, Rs, resolucion)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    rho = rho_c * np.exp(- (R**2) / (Rs**2))
    drho_dr = (-2 * R / Rs**2) * rho
    delta_quantum = delta_q * rho**2
    drho_dt = k_c2 * (drho_dr / (rho + delta_quantum + 1e-8))
    tiempo = np.cumsum(np.abs(drho_dt), axis=0)
    return tiempo

def exportar_campo_tiempo(campo, ruta="recursos/campo_dig_temp.png"):
    normalizado = (255 * (campo - np.min(campo)) / (np.ptp(campo))).astype(np.uint8)
    img = Image.fromarray(normalizado)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    img.save(ruta)
    return ruta
