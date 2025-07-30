from flask import Flask, render_template, request  # Importa Flask y funciones para renderizar HTML y manejar formularios
import math        # Biblioteca matemática para usar pi y potencias
import numpy as np # Biblioteca para trabajar con arreglos numéricos
import json        # Para enviar datos como JSON a la plantilla

app = Flask(__name__)  # Crea la instancia de la aplicación Flask

# Función para convertir unidades a centímetros
def convertir(valor, unidad):
    if unidad == "cm": return valor
    if unidad == "pulgadas": return valor * 2.54
    if unidad == "m": return valor * 100
    if unidad == "pies": return valor * 30.48
    return valor  # Si no coincide con ninguna, lo deja igual

# Ruta principal de la aplicación, acepta GET y POST
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = {}  # Diccionario vacío para guardar resultados
    plot_data = {}  # Diccionario vacío para datos de la gráfica

    if request.method == "POST":  # Si el usuario envió el formulario...
        # Obtiene los datos enviados desde el formulario HTML
        d = float(request.form["diametro"])
        l = float(request.form["lado"])
        dens = float(request.form["densidad"])
        costo = float(request.form["costo"])
        rendimineto_oblea = float(request.form["Rendimiento Por Oblea"]) #rendimineto por oblea
        ud = request.form["udiam"]
        ul = request.form["ulado"]

        # Convierte las unidades a centímetros
        d_cm = convertir(d, ud)
        l_cm = convertir(l, ul)

        # Cálculo de áreas y cantidades
        total = (math.pi*(d_cm/2)**2 / dens) - (math.pi * d_cm / (2*dens).sqrt(2) # Total de pastillas teóricas

        # Cálculo del rendimiento usando la fórmula con densidad de defectos
        rendimiento = rendimineto_oblea * (1 + (dens * area_chip / 4)) ** -4

        buenas = total * rendimiento                   # Pastillas buenas
        costo_unitario = costo / buenas                # Costo por pastilla buena

        # Guarda los resultados para mostrarlos en HTML
        resultado = {
            "wafer": round(area_wafer, 2),
            "chip": round(area_chip, 2),
            "total": int(total),
            "rendimiento": round(rendimiento * 100, 2),
            "buenas": int(buenas),
            "costo": round(costo_unitario, 2)
        }

        # ---- Sección de datos para la gráfica interactiva ----
        lados = np.arange(0.1, 2.05, 0.1).round(2).tolist()  # Genera lados de pastilla de 0.1 a 2.0 cm
        rendimientos = []
        costos = []

        for lado_val in lados:
            area = lado_val ** 2
            total_p = area_wafer / area
            yield_val = (1 + (dens * area / 4)) ** -4
            buenas = total_p * yield_val
            costo_p = costo / buenas
            rendimientos.append(round(yield_val * 100, 2))  # Guarda rendimiento en %
            costos.append(round(costo_p, 2))                # Guarda costo por pastilla

        # Empaqueta datos de la gráfica para enviarlos al template
        plot_data = {
            "lados": lados,
            "rendimientos": rendimientos,
            "costos": costos
        }

    # Renderiza la plantilla HTML con los resultados y la gráfica
    return render_template("index.html", resultado=resultado, plot_data=json.dumps(plot_data))

# Permite correr el servidor en entorno local o Render (puerto 10000)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=10000)
