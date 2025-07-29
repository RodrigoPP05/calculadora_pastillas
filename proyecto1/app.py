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
        ud = request.form["udiam"]
        ul = request.form["ulado"]

        d_cm = convertir(d, ud)
        l_cm = convertir(l, ul)

        area_wafer = math.pi * (d_cm / 2) ** 2
        area_chip = l_cm ** 2
        total = area_wafer / area_chip
        rendimiento = (1 + (dens * area_chip / 4)) ** -4
        buenas = total * rendimiento
        costo_unitario = costo / buenas

        resultado = {
            "wafer": round(area_wafer, 2),
            "chip": round(area_chip, 2),
            "total": int(total),
            "rendimiento": round(rendimiento * 100, 2),
            "buenas": int(buenas),
            "costo": round(costo_unitario, 2)
        }

        # Generar datos para gráficas
        lados = np.arange(0.1, 2.05, 0.1).round(2).tolist()
        rendimientos = []
        costos = []

        for lado_val in lados:
            area = lado_val ** 2
            total_p = area_wafer / area
            yield_val = (1 + (dens * area / 4)) ** -4
            buenas = total_p * yield_val
            costo_p = costo / buenas
            rendimientos.append(round(yield_val * 100, 2))
            costos.append(round(costo_p, 2))

        plot_data = {
            "lados": lados,
            "rendimientos": rendimientos,
            "costos": costos
        }

    return render_template("index.html", resultado=resultado, plot_data=json.dumps(plot_data))

if __name__ == "__main__":
    app.run(debug=True)
