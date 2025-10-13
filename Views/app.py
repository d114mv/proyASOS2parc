from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/algoritmo', methods=['POST'])
def seleccionar_algoritmo():
    algoritmo = request.form.get("algoritmo")
    print("Algoritmo seleccionado:", algoritmo)
    return f"<h2>Has seleccionado: {algoritmo}</h2><p>Próximamente se mostrará su formulario.</p>"

if __name__ == '__main__':
    app.run(debug=True)
