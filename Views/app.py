from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sys
import os

# Aseguramos que Python pueda importar simulator.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Simulacion")))
from simulator import Simulator  # Clase que maneja los algoritmos

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Guardamos una instancia del simulador
sim = None

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("start_simulation")
def handle_start_simulation(data):
    """
    data vendrá con algo como:
    {
        "algorithm": "FCFS",
        "processes": [
            {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
            {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1}
        ],
        "quantum": 2,
        "context_switch": 1
    }
    """
    global sim
    sim = Simulator(
        processes=data["processes"],
        algorithm=data["algorithm"],
        quantum=data.get("quantum"),
        context_switch=data.get("context_switch", 0)
    )

    # Emitimos paso a paso
    for tick_info in sim.run_step_by_step():
        socketio.emit("simulation_update", tick_info)

    # Al terminar, emitimos métricas finales
    results = sim.get_results()
    socketio.emit("simulation_finished", results)

if __name__ == "__main__":
    socketio.run(app, debug=True)