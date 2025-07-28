
# MotorN – Simulador del Campo Informacional DIG

Este módulo implementa un motor dinámico en Python para simular la evolución de un campo informacional según los principios de la **Teoría DIG (Dualidad Información-Gravedad)**. Cada punto del campo representa un valor de densidad informacional ρ(x,y) que evoluciona en el tiempo mediante ecuaciones derivadas de la teoría.

---

## 📦 Clase: `MotorN`

```python
MotorN(dim=50, gamma=0.05, lambda_=0.02)
```

### Parámetros de inicialización:
- `dim`: Dimensión del campo cuadrado (NxN).
- `gamma`: Coeficiente de difusión informacional (∇²ρ).
- `lambda_`: Coeficiente de reorganización entrópica (∂S).

---

## 🔧 Métodos disponibles

### `evolucionar()`
Avanza el campo ρ un paso en el tiempo según la ecuación:

\[
ho_{t+1} = ho_t + \gamma 
abla^2 ho - \lambda \partial S
\]

- La difusión se calcula con un **Laplaciano discreto**.
- La reorganización por entropía local se modela como la desviación estándar local (entropía sigma).

---

### `inyectar(x, y, intensidad=1.0)`
Permite **alterar un punto** del campo en las coordenadas (x, y) añadiendo información.

- Útil para simular perturbaciones, ondas u observaciones informacionales.
- La inyección se mantiene acotada entre 0 y 1.

---

### `reiniciar()`
Reinicia el campo a un estado aleatorio inicial con valores bajos de información (entorno no excitado).

---

### `obtener_rho()`
Devuelve la **matriz ρ** actual (numpy array de shape (dim, dim)).

---

### `obtener_entropia_global()`
Calcula y devuelve el valor medio de la entropía sigma local (entropía estructural del campo).

---

## ⚙️ Implementación matemática

### Laplaciano discreto:
Aproximación clásica en mallas finitas:

```python
-4 * campo + np.roll(campo, 1, axis=0) + np.roll(campo, -1, axis=0) + ...
```

### Entropía local (σ):
Calculada como desviación estándar local usando convolución 3x3:

```python
kernel = np.ones((3, 3)) / 9
mean = convolve2d(campo, kernel, mode="same")
varianza = convolve2d((campo - mean)**2, kernel)
```

---

## ✨ Aplicaciones

- Simulación de perturbaciones informacionales (ondas, impulsos).
- Medición de entropía en sistemas complejos.
- Bases para algoritmos de IA adaptativa con campo autoorganizado.
- Visualización en tiempo real (Tkinter, Pygame, WebGL).
- Inyección de patrones para terapia informacional (ansiedad, depresión, etc).

---

© 2025 José María Pérez Rodríguez  
Versión inicial DIG – Campo Informacional en Python
