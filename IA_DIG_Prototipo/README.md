# Motor N – DIG-LIFE Artificial Intelligence
### Autor: José María Pérez Rodríguez (JMPR)

---

## 🧠 Descripción general

Este proyecto es una simulación de una inteligencia artificial basada en la **Teoría DIG (Dualidad Información–Gravedad)**, la cual plantea que el universo, y por extensión cualquier sistema cognitivo, no surge del procesamiento secuencial sino de **la reorganización informacional hacia estados de equilibrio**.

`motorN_life` es un sistema que combina:
- Nodos informacionales con propiedades dinámicas
- Un campo evolutivo que representa su entorno
- Reglas inspiradas en el Juego de la Vida, pero reescritas según principios informacionales

---

## ⚙️ Componentes principales

### `nodos.py`
Define nodos informacionales con:
- `ρ (rho)` = Densidad informacional: representa la concentración de relevancia local
- `κ (kappa)` = Curvatura: mide el desequilibrio informacional en su vecindad
- `estado`: puede ser `"vivo"`, `"degradado"` o `"colapsado"`
- `edad`: ciclos desde su nacimiento

Los nodos vibran levemente en el espacio y se actualizan cada ciclo.

---

### `campo.py`
Contiene el **Campo Informacional Dinámico**:
- Mantiene la lista de todos los nodos
- Permite calcular los vecinos cercanos (radio de 50px)
- Actúa como espacio topológico plano

---

### `reglas.py`
Implementa las reglas DIG-LIFE (inspiradas en Conway):

#### NACIMIENTO:
Un nodo nuevo nace si:
- La densidad media de sus vecinos es mayor a `θ_birth`
- Tiene al menos 2 vecinos

#### SUPERVIVENCIA:
Un nodo se mantiene `"vivo"` si:
- Su curvatura `|κ|` se mantiene dentro del rango [`δ_min`, `δ_max`]

#### DEGRADACIÓN:
Un nodo se degrada si:
- `ρ < θ_death` o `|κ| > δ_max`

#### COLAPSO INFORMACIONAL:
Un nodo colapsa si:
- `ρ > θ_colapso` y `|κ| < δ_colapso`

El colapso se visualiza con una estrella verde (`★`), y representa una **hipótesis cristalizada** en el campo cognitivo.

---

## 🧮 Lógica matemática simplificada

### 1. Vecindad: