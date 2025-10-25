# 🧠 Simulador de Algoritmos de Planificación de Procesos

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

Una aplicación web interactiva para simular y visualizar **algoritmos de planificación de procesos** en sistemas operativos, desarrollada como proyecto académico.

## 🚀 Características Principales

### ⚡ Algoritmos Implementados
* **⚙️ FCFS (First Come First Served)**: Planificación por orden de llegada
* **📊 SJF (Shortest Job First)**: Ejecuta primero los procesos más cortos (no preemptivo)
* **🔄 Round Robin**: Planificación con quantum configurable
* **🎯 Prioridad**: Planificación por niveles de prioridad
* **⚡ SRT (Shortest Remaining Time)**: Versión preemptiva de SJF

### 🎯 Funcionalidades Avanzadas
* ✅ **Interfaz web moderna** y completamente responsive
* ✅ **Entrada dinámica** de procesos con validación
* ✅ **Visualización interactiva** con diagramas de Gantt
* ✅ **Controles de simulación** (avanzar, retroceder, pausar)
* ✅ **Cálculo de métricas** en tiempo real
* ✅ **Explicaciones educativas** detalladas de cada algoritmo
* ✅ **Configuración flexible** de parámetros (quantum, cambio de contexto)

## 📊 Métricas Calculadas

* ⏱️ **Tiempo de Retorno Promedio** (Turnaround Time)
* ⏳ **Tiempo de Espera Promedio** (Waiting Time)
* 🚀 **Throughput** (Procesos completados por unidad de tiempo)
* 🔄 **Secuencia de Ejecución** completa
* 📈 **Diagramas de Gantt** interactivos y animados

## 🛠️ Instalación y Configuración

### 📋 Prerrequisitos
* Python **3.8 o superior**
* pip (gestor de paquetes de Python)
* Navegador web moderno

### ⚙️ Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone https://github.com/d114mv/proyASOS2parc.git
   cd proyASOS2parc

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt

3. **Ejecutar la aplicación**
   ```bash
   streamlit run app.py

4. **Abrir en el navegador**
   http://localhost:8501

## 📁 Estructura del Proyecto
* proyecto_planificacion/
* ├── app.py                          # Aplicación principal Streamlit
* ├── pages/                          # Páginas de la aplicación
* │   ├── 1_🏠_Inicio.py             # Página de presentación
* │   ├── 2_⚙️_FCFS.py               # Simulador First Come First Served
* │   ├── 3_📊_SJF.py                # Simulador Shortest Job First
* │   ├── 4_🔄_Round_Robin.py        # Simulador Round Robin
* │   ├── 5_🎯_Prioridad.py          # Simulador Planificación por Prioridad
* │   └── 6_⚡_SRT.py                # Simulador Shortest Remaining Time
* ├── utils/                          # Módulos de lógica de negocio
* │   ├── __init__.py                # Paquete Python
* │   ├── fcfs.py                    # Algoritmo FCFS
* │   ├── sjf.py                     # Algoritmo SJF
* │   ├── rr.py                      # Algoritmo Round Robin
* │   ├── prioridad.py               # Algoritmo Prioridad
* │   ├── srt.py                     # Algoritmo SRT
* │   ├── visualizacion.py           # Funciones de visualización unificadas
* │   └── helpers.py                 # Funciones auxiliares comunes
* ├── datos_temporales.py            # Datos de procesos (generado automáticamente)
* ├── requirements.txt               # Dependencias del proyecto
* └── README.md                      # Este archivo


## 🎮 Guía de Uso
### Para FCFS (First Come First Served)
* Navega a la sección "⚙️ FCFS"
* Define el número de procesos
* Establece tiempos de llegada y duración para cada proceso
* Haz clic en "Ejecutar Simulación FCFS"
* Analiza la secuencia de ejecución por orden de llegada

### Para SJF (Shortest Job First)
* Navega a la sección "📊 SJF"
* Define el número de procesos
* Establece las duraciones de cada proceso
* Haz clic en "Ejecutar Simulación SJF"
* Observa cómo se ejecutan primero los procesos más cortos

### Para Round Robin
* Navega a la sección "🔄 Round Robin"
* Configura el tamaño del quantum
* Opcional: activa cambio de contexto
* Define los procesos con sus llegadas y duraciones
* Ejecuta la simulación y observa la rotación entre procesos

### Para Planificación por Prioridad
* Navega a la sección "🎯 Prioridad"
* Define prioridades (0 = máxima prioridad)
* Establece llegadas y duraciones
* Ejecuta y observa cómo se priorizan los procesos importantes

### Para SRT (Shortest Remaining Time)
* Navega a la sección "⚡ SRT"
* Define procesos con diferentes tiempos de llegada
* Ejecuta la simulación
* Observa las preempciones cuando llegan procesos más cortos


## 👥 Equipo de Desarrollo
### Desarrollado por:

* 🧑‍💻 Muriel Vargas Dilan Itamar
* 🧑‍💻 Quintana Callejas Marco Antonio
* 🧑‍💻 Murillo Rodriguez Juan Rodolfo
* 🧑‍💻 Aduviri Calizaya Leonel


## 📚 Explicación de Algoritmos
### ⚙️ FCFS (First Come First Served)
* No preemptivo - Ejecuta procesos en estricto orden de llegada.
* ✅ Ventajas:
* Simple de implementar
* Justo en términos de orden de llegada
* Bajo overhead del sistema
* ❌ Desventajas:
* Efecto convoy (procesos largos retrasan cortos)
* Poco responsivo para procesos interactivos

### 📊 SJF (Shortest Job First)
* No preemptivo - Ejecuta primero los procesos con menor duración.
* ✅ Ventajas:
* Minimiza tiempo de espera promedio
* Eficiente para lotes de procesos
* ❌ Desventajas:
* Inanición para procesos largos
* Requiere conocer duraciones de antemano

### 🔄 Round Robin
* Preemptivo - Asigna quantum de tiempo a cada proceso.
* ✅ Ventajas:
* Justo para todos los procesos
* Excelente para sistemas interactivos
* Evita la inanición
* ❌ Desventajas:
* Rendimiento depende del quantum seleccionado
* Overhead por cambios de contexto frecuentes

### 🎯 Planificación por Prioridad
* Puede ser preemptivo o no - Ejecuta basado en niveles de prioridad.
* ✅ Ventajas:
* Flexible para diferentes necesidades
* Adecuado para sistemas en tiempo real
* Puede combinarse con otros algoritmos
* ❌ Desventajas:
* Inanición para prioridades bajas
* Subjetivo al definir prioridades

### ⚡ SRT (Shortest Remaining Time)
* Preemptivo - Siempre ejecuta el proceso con menor tiempo restante.
* ✅ Ventajas:
* Excelente tiempo de respuesta
* Minimiza tiempos de espera
* Óptimo para procesos cortos
* ❌ Desventajas:
* Alto overhead por cambios de contexto
* Inanición posible para procesos largos


## 🐛 Solución de Problemas
### Error: "ModuleNotFoundError"
* Asegúrate de tener instaladas todas las dependencias
   ```bash
   pip install --upgrade -r requirements.txt

### Error: "Port already in use"
* Ejecutar en un puerto diferente
   ```bash
   streamlit run app.py --server.port 8502

### La aplicación no se abre
* Verifica que Python 3.8+ esté correctamente instalado
* Asegúrate de estar en el directorio correcto del proyecto
* Revisa que no haya firewalls bloqueando el puerto

### Problemas de visualización
* Actualiza tu navegador a la versión más reciente
* Limpia la caché del navegador
* Verifica que JavaScript esté habilitado

## 🔧 Tecnologías Utilizadas
* Frontend: Streamlit
* Visualización: Matplotlib
* Procesamiento de datos: Pandas, NumPy
* Lenguaje: Python 3.8+
* Estilos: CSS personalizado

## 📄 Licencia
* Este proyecto es desarrollado con fines educativos como parte de un trabajo académico en la materia de Administración de Sistemas Operativos y Servidores de la Escuela Militar de Ingeniería U.A. Cochabamba.

## 🤝 Contribuciones
* Las contribuciones son bienvenidas. Si encuentras algún error o tienes sugerencias de mejora, no dudes en crear un issue o pull request.

## ⭐ Apoya el Proyecto
* Si este proyecto te fue útil para entender los algoritmos de planificación, considera darle una estrella en GitHub para apoyar el trabajo del equipo.

### ¡Disfruta explorando el fascinante mundo de la planificación de procesos! 🎉