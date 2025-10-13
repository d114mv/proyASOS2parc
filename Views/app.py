from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_simulation():
    data = request.get_json()
    print("Procesos recibidos:", data)
    # Aquí luego llamaremos a simulator.py para procesar los algoritmos
    return jsonify({"status": "ok", "message": "Simulación iniciada correctamente"})

if __name__ == '__main__':
    socketio.run(app, debug=True)
