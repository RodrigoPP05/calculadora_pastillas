# Importación de librerías necesarias
from flask import Flask, render_template, request  # Flask y módulos para manejar rutas y formularios
import math        # Para operaciones matemáticas como pi y raíz cuadrada
import numpy as np # Para generar listas de valores y cálculos numéricos
import json        # Para convertir los datos a formato JSON y usarlos en JavaScript

# Se crea la aplicación Flask
app = Flask(__name__)

# Función para convertir diferentes unidades de longitud a centímetros
def convertir(valor, unidad):
    if unidad == "cm": return valor
    if unidad == "pulgadas": return valor * 2.54
    if unidad == "m": return valor * 100
    if unidad == "pies": return valor * 30.48
    return valor  # Por defecto, retorna el valor sin cambios

# Ruta para manejar los ejercicios adicionales
@app.route("/ejercicio", methods=["POST"])
def ejercicio():
    tipo = request.form.get("tipo")  # Se obtiene el tipo de ejercicio desde el formulario

    # Cálculo del costo por pastilla
    if tipo == "pastilla":
        oblea = float(request.form["oblea"])
        num = int(request.form["num"])
        rendimiento = float(request.form["rendimiento"]) / 100
        resultado = oblea / (num * rendimiento)
        return {"resultado": round(resultado, 4)}

    # Cálculo del precio de una oblea conociendo el precio por pastilla
    elif tipo == "oblea_para_precio":
        precio = float(request.form["precio"])
        num = int(request.form["num"])
        rendimiento = float(request.form["rendimiento"]) / 100
        resultado = precio * num * rendimiento
        return {"resultado": round(resultado, 4)}

    # Cálculo del costo del circuito integrado (IC)
    elif tipo == "ic":
        die = float(request.form["die"])
        prueba = float(request.form["prueba"])
        empaque = float(request.form["empaque"])
        rendimiento_final = float(request.form["rend_final"]) / 100
        resultado = (die + prueba + empaque) / rendimiento_final
        return {"resultado": round(resultado, 4)}

    # Comparación entre un costo original y uno nuevo
    elif tipo == "comparacion":
        original = float(request.form["original"])
        nuevo = float(request.form["nuevo"])
        prueba = float(request.form["prueba"])
        empaque = float(request.form["empaque"])
        rendimiento_final = float(request.form["rend_final"]) / 100
        anterior = (original + prueba + empaque) / rendimiento_final
        nuevo_total = (nuevo + prueba + empaque) / rendimiento_final
        factor = nuevo_total / anterior
        return {
            "anterior": round(anterior, 4),
            "nuevo": round(nuevo_total, 4),
            "factor": round(factor, 2)
        }

    # En caso de que el tipo de ejercicio no sea válido
    return {"error": "Tipo de ejercicio no válido"}, 400

# Ruta principal del sitio, acepta GET y POST
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = {}    # Diccionario para guardar los resultados numéricos
    plot_data = {}    # Diccionario para guardar datos para gráficas

    if request.method == "POST":
        # Entrada de datos del formulario
        d = float(request.form["diametro"])
        l = float(request.form["lado"])
        dens = float(request.form["densidad"])
        costo = float(request.form["costo"])
        rendimiento_oblea = float(request.form["Rendimiento Por Oblea"] or 100) / 100
        ud = request.form["udiam"]  # Unidad del diámetro
        ul = request.form["ulado"]  # Unidad del lado

        # Conversiones de unidades a centímetros
        d_cm = convertir(d, ud)
        l_cm = convertir(l, ul)

        # Cálculo del área de la oblea y del chip (pastilla)
        area_wafer = math.pi * (d_cm / 2) ** 2
        area_chip = l_cm ** 2

        # Estimación del número de pastillas por oblea (fórmula corregida)
        total = ((math.pi * (d_cm/2)**2) / area_chip) - (math.pi * d_cm) / math.sqrt(2 * area_chip)

        # Cálculo del rendimiento ajustado de la oblea (yield con defectos)
        rendimiento = rendimiento_oblea * (1 + (dens * area_chip / 4)) ** -4

        # Cálculo de buenas pastillas y del costo unitario por pastilla
        buenas = total * rendimiento
        costo_unitario = costo / buenas

        # Verificar si se usarán costos extras de prueba/empaque
        usar_costos_extra = request.form.get("usar_extra") == "on"
        costo_prueba = float(request.form.get("costo_prueba") or 0)
        costo_empaque = float(request.form.get("costo_empaque") or 0)
        rendimiento_final = float(request.form.get("rend_final") or 100) / 100

        # Cálculo opcional del costo del circuito integrado
        costo_die = costo_unitario
        costo_ic = None
        if usar_costos_extra:
            costo_ic = (costo_die + costo_prueba + costo_empaque) / rendimiento_final

        # Se prepara el diccionario de resultados para mostrar en HTML
        resultado = {
            "wafer": round(area_wafer, 2),
            "chip": round(area_chip, 2),
            "total": int(total),
            "rendimiento": round(rendimiento * 100, 2),
            "buenas": int(buenas),
            "costo": round(costo_unitario, 4),
        }

        if costo_ic is not None:
            resultado["costo_ic"] = round(costo_ic, 4)

        # Cálculo de datos para graficar rendimiento y costo en función del tamaño del chip
        lados = np.arange(0.1, 2.05, 0.1).round(2).tolist()
        rendimientos = []
        costos = []

        for lado_val in lados:
            area = lado_val ** 2
            total_p = ((math.pi * (d_cm/2)**2) / area) - (math.pi * d_cm) / math.sqrt(2 * area)
            rendimiento_est = rendimiento_oblea * (1 + (dens * area / 4)) ** -4
            buenas = total_p * rendimiento_est
            costo_p = costo / buenas
            rendimientos.append(round(rendimiento_est * 100, 2))
            costos.append(round(costo_p, 4))

        # Se empaquetan los datos para enviarlos al HTML como JSON
        plot_data = {
            "lados": lados,
            "rendimientos": rendimientos,
            "costos": costos
        }

    # Renderiza el template 'index.html' con los resultados y datos de la gráfica
    return render_template("index.html", resultado=resultado, plot_data=json.dumps(plot_data))

# Punto de entrada principal de la app
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Puerto por defecto 5000
    app.run(host='0.0.0.0', port=10000)  # Se ejecuta en el puerto 10000
