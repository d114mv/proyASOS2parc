# 🧠 Simulador de Algoritmos de Planificación de Procesos

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-square&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-square&logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-square&logo=Matplotlib&logoColor=black)

Una aplicación web interactiva para simular y visualizar **algoritmos de planificación de procesos** en sistemas operativos.

---

## 🚀 Características

### ⚡ Algoritmos Implementados
- **SRT (Shortest Remaining Time)**: versión *preemptiva* que ejecuta el proceso con menor tiempo restante.
- **SJF (Shortest Job First)**: versión *no preemptiva* que ejecuta primero los procesos más cortos.

### 🎯 Funcionalidades
- ✅ **Interfaz web moderna** y responsive.  
- ✅ **Entrada dinámica** de procesos.  
- ✅ **Visualización con diagramas de Gantt.**  
- ✅ **Cálculo de métricas** en tiempo real.  
- ✅ **Explicaciones detalladas** de cada algoritmo.  
- ✅ **Navegación intuitiva** entre secciones.  

---

## 📊 Métricas Calculadas

- ⏱️ **Tiempo de espera promedio**
- 🔄 **Tiempo de retorno promedio**
- 💻 **Utilización de CPU**
- 📈 **Diagramas de Gantt** interactivos

---

## 🛠️ Instalación

### 📋 Prerrequisitos
- Python **3.8 o superior**
- pip (gestor de paquetes de Python)

---

### ⚙️ Pasos de instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone https://github.com/d114mv/proyASOS2parc.git
   cd proyASOS2parc

2. **Instalar dependencias**
pip install -r requirements.txt

3. **Ejecutar la aplicación**
py -m streamlit run app.py

4. **Abrir en el navegador**
http://localhost:8501

--

# 📁 Estructura del Proyecto
proyecto_planificacion/
├── app.py                 # Aplicación principal
├── pages/                 # Páginas de la aplicación
│   ├── 1_🏠_Inicio.py    # Página de inicio
│   ├── 2_⚡_SRT.py       # Simulador SRT
│   └── 3_🟡_SJF.py       # Simulador SJF
├── utils/                 # Módulos de lógica
│   ├── srt.py            # Algoritmo SRT
│   ├── sjf.py            # Algoritmo SJF
│   └── visualizacion.py  # Funciones de gráficos
├── requirements.txt       # Dependencias
└── README.md             # Este archivo

--

## 🎮 Cómo Usar
### Para SRT (Shortest Remaining Time)

- Navega a la sección "⚡ SRT"
- Define el número de procesos
- Establece tiempos de llegada y duración para cada proceso
- Haz clic en "Ejecutar Simulación SRT"
- Analiza los resultados y el diagrama de Gantt

### Para SJF (Shortest Job First)

- Navega a la sección "🟡 SJF"
- Define el número de procesos
- Establece las duraciones de cada proceso
- Haz clic en "Ejecutar Simulación SJF"
- Revisa la secuencia de ejecución y métricas

--

## 👥 Desarrollado por

- Muriel Vargas Dilan Itamar
- Quintana Callejas Marco Antonio
- Murillo Rodriguez Juan Rodolfo
- Aduviri Calizaya Leonel

--

## 📚 Explicación de Algoritmos

⚡ SRT (Shortest Remaining Time)
Algoritmo preemptivo que en cada instante selecciona el proceso con menor tiempo restante de ejecución. Ideal para minimizar tiempos de respuesta pero puede causar inanición en procesos largos.

🟡 SJF (Shortest Job First)
Algoritmo no preemptivo que ejecuta los procesos en orden de duración creciente. Minimiza el tiempo de espera promedio pero requiere conocer las duraciones de antemano.

--

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
Asegúrate de tener instaladas todas las dependencias
pip install --upgrade -r requirements.txt

### Error: "Port already in use"
Ejecutar en un puerto diferente
streamlit run app.py --server.port 8502

### La aplicación no se abre
Verifica que Python esté correctamente instalado
Asegúrate de estar en el directorio correcto del proyecto
Revisa que no haya firewalls bloqueando el puerto 8501

--

## 🔧 Tecnologías Utilizadas
- Frontend: Streamlit
- Gráficos: Matplotlib
- Procesamiento: NumPy
- Lenguaje: Python

--

## 📄 Licencia
Este proyecto es con fines educativos como parte de un trabajo académico.

--

## ⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!