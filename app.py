
from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "data/reporteadores.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"].strip().lower()
        reportador = request.form["reportador"].strip().lower()
        data = load_data()

        if nombre not in data:
            data[nombre] = reportador
            save_data(data)

        return redirect(f"/ver?nombre={nombre}")

    return render_template("index.html")


@app.route("/ver")
def ver():
    nombre = request.args.get("nombre", "").strip().lower()
    data = load_data()
    reportador = data.get(nombre)
    return render_template("ver.html", nombre=nombre, reportador=reportador)


@app.route("/api/data")
def api_data():
    return jsonify(load_data())


if __name__ == "__main__":
    app.run(debug=True)
