from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Ruta principal: menú de selección de algoritmo
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para redirigir a la interfaz de cada algoritmo
@app.route('/algoritmo', methods=['POST'])
def seleccionar_algoritmo():
    algoritmo = request.form.get("algoritmo")
    # Por ahora solo imprimimos en consola y redirigimos a la misma página
    print("Algoritmo seleccionado:", algoritmo)
    # Aquí luego llamaremos al formulario web de cada algoritmo
    return f"<h2>Has seleccionado: {algoritmo}</h2><p>Próximamente se mostrará su formulario.</p>"

if __name__ == '__main__':
    app.run(debug=True)
