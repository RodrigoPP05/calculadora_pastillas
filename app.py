from flask import Flask, render_template, request
import math
import numpy as np
import json

app = Flask(__name__)

def convertir(valor, unidad):
    if unidad == "cm": return valor
    if unidad == "pulgadas": return valor * 2.54
    if unidad == "m": return valor * 100
    if unidad == "pies": return valor * 30.48
    return valor

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = {}
    plot_data = {}

    if request.method == "POST":
        d = float(request.form["diametro"])
        l = float(request.form["lado"])
        dens = float(request.form["densidad"])
        costo = float(request.form["costo"])
        rendimiento_oblea = float(request.form["Rendimiento Por Oblea"] or 100) / 100
        ud = request.form["udiam"]
        ul = request.form["ulado"]

        d_cm = convertir(d, ud)
        l_cm = convertir(l, ul)

        area_wafer = math.pi * (d_cm / 2) ** 2
        area_chip = l_cm ** 2
        total = (math.pi * d_cm**2) / area_chip - (math.pi * d_cm) / math.sqrt(2 * area_chip)

        rendimiento = rendimiento_oblea * (1 + (dens * area_chip / 4)) ** -4
        buenas = total * rendimiento
        costo_unitario = costo / buenas

        # Nuevos parámetros opcionales para costo IC
        usar_costos_extra = request.form.get("usar_costos_extra") == "si"
        costo_prueba = float(request.form.get("costo_prueba", 0))
        costo_empaque = float(request.form.get("costo_empaque", 0))
        rendimiento_final = float(request.form.get("rendimiento_final", 100)) / 100

        costo_die = costo_unitario
        costo_ic = None

        if usar_costos_extra:
            costo_ic = (costo_die + costo_prueba + costo_empaque) / rendimiento_final

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

        lados = np.arange(0.1, 2.05, 0.1).round(2).tolist()
        rendimientos = []
        costos = []

        for lado_val in lados:
            area = lado_val ** 2
            total_p = (math.pi * d_cm**2) / area - (math.pi * d_cm) / math.sqrt(2 * area)
            rendimiento_est = rendimiento_oblea * (1 + (dens * area / 4)) ** -4
            buenas = total_p * rendimiento_est
            costo_p = costo / buenas
            rendimientos.append(round(rendimiento_est * 100, 2))
            costos.append(round(costo_p, 4))

        plot_data = {
            "lados": lados,
            "rendimientos": rendimientos,
            "costos": costos
        }

    return render_template("index.html", resultado=resultado, plot_data=json.dumps(plot_data))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=10000)
