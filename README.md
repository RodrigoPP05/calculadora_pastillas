# calculadora_pastillas

# 💊 Calculadora de Pastillas de Silicio – Flask App

Una aplicación web interactiva desarrollada con **Flask**, **HTML/CSS**, **JavaScript** y **Plotly**, que permite calcular:

- El rendimiento de fabricación de pastillas (dies) a partir de una oblea de silicio.
- El costo por pastilla buena.
- El costo del circuito integrado (IC) incluyendo pruebas y empaquetado.
- Comparaciones entre diferentes configuraciones de costos.

---

## 🌐 Vista previa

<img src="static/demo.png" alt="Demo App" width="600"/>

---

## 🚀 Características

✅ Cálculo automático del rendimiento según la densidad de defectos  
✅ Conversión de unidades (cm, m, pulgadas, pies)  
✅ Modo educativo interactivo para practicar con ejercicios teóricos  
✅ Gráfica dinámica: Costo y rendimiento en función del tamaño de la pastilla  
✅ Historial de cálculos en la sesión  
✅ UI moderna, responsiva y con compatibilidad offline (via Service Worker)  

---

## 🧮 Fórmulas Implementadas

**Número de pastillas por oblea:**

\[
\text{Pastillas} = \frac{\pi \cdot (D/2)^2}{L^2} - \frac{\pi \cdot D}{\sqrt{2 \cdot L^2}}
\]

**Rendimiento con defectos:**

\[
Y = Y_0 \cdot \left(1 + \frac{D \cdot A}{4}\right)^{-4}
\]

**Costo por pastilla buena:**

\[
C = \frac{\text{Costo oblea}}{\text{Pastillas buenas}}
\]

**Costo del circuito integrado (IC):**

\[
C_{\text{IC}} = \frac{C_{\text{die}} + C_{\text{prueba}} + C_{\text{empaque}}}{\text{Rend. final}}
\]

---

## 📦 Instalación local

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/calculadora-pastillas.git
cd calculadora-pastillas
