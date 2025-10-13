from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/algoritmo', methods=['POST'])
def seleccionar_algoritmo():
    algoritmo = request.form.get("algoritmo")
    if algoritmo == "FCFS":
        return redirect(url_for("fcfs"))
    elif algoritmo == "SJF":
        return redirect(url_for("sjf"))
    elif algoritmo == "SRT":
        return redirect(url_for("srt"))
    elif algoritmo == "Prioridades":
        return redirect(url_for("prioridad"))
    elif algoritmo == "Round Robin":
        return redirect(url_for("rr"))
    else:
        return "<h2>Algoritmo no válido</h2>"

# ---------- Formularios web de cada algoritmo ----------
@app.route('/fcfs', methods=['GET', 'POST'])
def fcfs():
    if request.method == "POST":
        procesos = request.form.getlist("procesos")
        # Aquí se procesarían los datos o se guardan en archivo para simular
        return f"<h2>FCFS Procesos: {procesos}</h2>"
    return render_template("fcfs.html")

@app.route('/sjf', methods=['GET', 'POST'])
def sjf():
    if request.method == "POST":
        procesos = request.form.getlist("procesos")
        return f"<h2>SJF Procesos: {procesos}</h2>"
    return render_template("sjf.html")

@app.route('/srt', methods=['GET', 'POST'])
def srt():
    if request.method == "POST":
        procesos = request.form.getlist("procesos")
        return f"<h2>SRT Procesos: {procesos}</h2>"
    return render_template("srt.html")

@app.route('/prioridad', methods=['GET', 'POST'])
def prioridad():
    if request.method == "POST":
        procesos = request.form.getlist("procesos")
        prioridades = request.form.getlist("prioridades")
        return f"<h2>Prioridades: {list(zip(procesos, prioridades))}</h2>"
    return render_template("prioridad.html")

@app.route('/rr', methods=['GET', 'POST'])
def rr():
    if request.method == "POST":
        procesos = request.form.getlist("procesos")
        quantum = request.form.get("quantum")
        return f"<h2>Round Robin - Quantum: {quantum}, Procesos: {procesos}</h2>"
    return render_template("rr.html")

if __name__ == '__main__':
    app.run(debug=True)
