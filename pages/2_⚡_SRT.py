import streamlit as st
import pandas as pd
from utils.srt import calcular_srt
from utils.visualizacion import generar_visualizacion_srt

# --- Configuración de la Página ---
st.set_page_config(layout="wide", page_title="Simulador SRT")
st.title("⚡ Simulador de Planificación - SRT (Shortest Remaining Time)")
st.caption("Algoritmo Preemptivo - Ejecuta el proceso con menor tiempo restante")

# --- 1. Sección de Entrada de Datos ---
st.header("1. Ingrese los Procesos")

# Inicializar datos en session_state
if 'procesos_srt' not in st.session_state:
    st.session_state.procesos_srt = pd.DataFrame([
        {"llegada": 0, "duracion": 5},
        {"llegada": 1, "duracion": 3},
        {"llegada": 2, "duracion": 8},
        {"llegada": 3, "duracion": 2},
    ])

# Editor de datos para SRT
edited_df = st.data_editor(
    st.session_state.procesos_srt,
    num_rows="dynamic",
    column_config={
        "llegada": st.column_config.NumberColumn("Tiempo de Llegada", min_value=0, required=True),
        "duracion": st.column_config.NumberColumn("Duración (CPU)", min_value=1, required=True),
    },
    key="srt_data_editor"
)

# Guardar cambios
st.session_state.procesos_srt = edited_df

# --- 2. Sección de Control de Simulación ---
if st.button("▶ Iniciar Simulación SRT", type="primary"):
    # Convertir DataFrame a lista de diccionarios
    procesos_list = edited_df.to_dict('records')
    
    if not procesos_list:
        st.error("Por favor, agregue al menos un proceso.")
    else:
        # Calcular SRT
        procesos_calculados = calcular_srt(procesos_list)
        
        # Guardar en session_state
        st.session_state.procesos_calculados = procesos_calculados
        st.session_state.tiempo_total = max(p['final'] for p in procesos_calculados)
        st.session_state.tiempo_actual = 0
        st.session_state.simulacion_iniciada = True
        st.rerun()

# --- 3. Sección de Visualización ---
if st.session_state.get("simulacion_iniciada", False):
    st.header("2. Visualización de la Simulación SRT")
    
    # Obtener datos actuales
    tiempo_actual = st.session_state.tiempo_actual
    tiempo_total = st.session_state.tiempo_total
    
    # Mostrar tiempo actual y controles
    st.subheader(f"⏰ Tiempo Actual: {tiempo_actual}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    if col1.button("⟲ Reiniciar"):
        st.session_state.tiempo_actual = 0
        st.rerun()

    if col2.button("◀ Retroceder"):
        if st.session_state.tiempo_actual > 0:
            st.session_state.tiempo_actual -= 1
            st.rerun()

    if col3.button("Avanzar ▶"):
        if st.session_state.tiempo_actual < tiempo_total:
            st.session_state.tiempo_actual += 1
            st.rerun()

    if col4.button("▶▶ Ver Todo"):
        st.session_state.tiempo_actual = tiempo_total
        st.rerun()

    # --- Generación del Gráfico SRT ---
    fig = generar_visualizacion_srt(
        st.session_state.procesos_calculados,
        st.session_state.tiempo_actual
    )
    
    # Mostrar gráfico
    st.pyplot(fig)

    # Mostrar datos calculados
    with st.expander("📊 Ver datos calculados de los procesos"):
        st.dataframe(st.session_state.procesos_calculados)

# --- 4. Información Educativa ---
with st.expander("📚 ¿Cómo funciona el Algoritmo SRT?"):
    st.markdown("""
    **⚡ SRT (Shortest Remaining Time) - Tiempo Restante Más Corto**

    **Características Principales:**
    - ✅ **Preemptivo**: Puede interrumpir procesos en ejecución
    - 🎯 **Selección inteligente**: Siempre elige el proceso con menor tiempo restante
    - ⏱️ **Excelente respuesta**: Minimiza tiempos de respuesta
    - 🔄 **Reevaluación constante**: En cada llegada de proceso

    **Cómo funciona paso a paso:**
    1. **En cada unidad de tiempo**, verifica qué procesos han llegado
    2. **Actualiza la cola** de procesos listos para ejecutar
    3. **Selecciona el proceso** con menor tiempo restante de ejecución
    4. **Si llega un proceso más corto**, puede interrumpir el actual
    5. **Ejecuta por 1 unidad** y actualiza tiempos restantes
    6. **Repite** hasta que todos los procesos terminen

    **Ventajas:**
    - Tiempos de respuesta muy cortos
    - Eficiente para mezclas de procesos largos y cortos
    - Más justo que FCFS para procesos cortos

    **Desventajas:**
    - ⚠️ Posibilidad de inanición para procesos largos
    - ⚠️ Overhead por cambios de contexto frecuentes
    - ⚠️ Requiere estimar tiempos de ejecución

    **Ejemplo de aplicación:**
    - Sistemas interactivos donde el tiempo de respuesta es crítico
    - Entornos con mezcla de procesos cortos y largos
    - Cuando se puede estimar razonablemente los tiempos de CPU
    """)

# Navegación en sidebar
with st.sidebar:
    st.header("🧭 Navegación")
    if st.button("🏠 Volver al Inicio"):
        st.switch_page("app.py")
    
    st.header("ℹ️ Acerca de SRT")
    st.info("""
    **SRT es óptimo para:**
    - Minimizar tiempo de respuesta
    - Procesos con diferentes duraciones
    - Entornos donde llegan procesos en diferentes momentos
    
    **Complejidad:** O(n log n) por reevaluación
    """)