import streamlit as st
import pandas as pd
from utils.srt import ejecutar_srt, crear_grafico_srt, calcular_metricas_srt

st.set_page_config(
    page_title="SRT - Simulador Planificación",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Algoritmo SRT (Shortest Remaining Time)")

st.markdown("""
El algoritmo **SRT (Shortest Remaining Time)** es una versión preemptiva de SJF que siempre 
ejecuta el proceso con el **menor tiempo restante de ejecución**.
""")

# Sidebar para información
with st.sidebar:
    st.header("ℹ️ Acerca de SRT")
    st.info("""
    **Características:**
    - ✅ Preemptivo
    - ✅ Minimiza tiempo de respuesta
    - ✅ Óptimo para tiempos cortos
    - ❌ Inanición posible
    - ❌ Complejo de implementar
    """)
    
    if st.button("🏠 Volver al Inicio"):
        st.switch_page("app.py")

# Entrada de datos
st.header("📥 Configuración de Procesos")

col1, col2 = st.columns([2, 1])

with col1:
    num_procesos = st.number_input(
        "Número de procesos", 
        min_value=1, 
        max_value=8, 
        value=4,
        help="Selecciona cuántos procesos quieres simular"
    )

with col2:
    st.markdown("### 💡 Tip")
    st.caption("SRT funciona mejor con procesos de diferentes duraciones y tiempos de llegada escalonados")

# Formulario dinámico para procesos
st.subheader("✏️ Definir Procesos")

procesos = []
cols = st.columns(4)

for i in range(num_procesos):
    with cols[i % 4]:
        st.markdown(f"**Proceso {i}**")
        llegada = st.number_input(
            f"Llegada P{i}", 
            min_value=0, 
            value=i,  # Llegadas escalonadas por defecto
            key=f"llegada_{i}"
        )
        duracion = st.number_input(
            f"Duración P{i}", 
            min_value=1, 
            value=(i+1)*2,  # Duraciones variadas por defecto
            key=f"duracion_{i}"
        )
        
        procesos.append({
            'pid': i,
            'llegada': llegada,
            'duracion': duracion
        })

# Mostrar resumen de procesos
if procesos:
    st.subheader("📋 Resumen de Procesos")
    df_procesos = pd.DataFrame(procesos)
    df_procesos['Proceso'] = df_procesos['pid'].apply(lambda x: f'P{x}')
    st.dataframe(df_procesos[['Proceso', 'llegada', 'duracion']], use_container_width=True)

# Ejecutar simulación
st.header("🎯 Simulación")

if st.button("🚀 Ejecutar Simulación SRT", type="primary"):
    if procesos:
        with st.spinner("Ejecutando algoritmo SRT..."):
            # Ejecutar algoritmo
            resultado = ejecutar_srt(procesos)
            
            # Mostrar resultados
            col1, col2, col3 = st.columns(3)
            
            metricas = calcular_metricas_srt(resultado)
            
            with col1:
                st.metric(
                    "⏱️ Tiempo de espera promedio", 
                    f"{metricas['espera_promedio']:.2f}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "🔄 Tiempo de retorno promedio", 
                    f"{metricas['retorno_promedio']:.2f}",
                    delta=None
                )
            
            with col3:
                st.metric(
                    "💻 Utilización de CPU", 
                    f"{metricas['utilizacion_cpu']:.1f}%",
                    delta=None
                )
            
            # Mostrar gráfico
            st.subheader("📊 Diagrama de Gantt y Resultados")
            fig = crear_grafico_srt(resultado)
            st.pyplot(fig)
            
            # Mostrar detalles de ejecución
            st.subheader("🔍 Detalles de Ejecución")
            for proc in resultado:
                with st.expander(f"Proceso P{proc['pid']} - {len(proc['ejecuciones'])} segmentos"):
                    st.write(f"**Llegada:** {proc['llegada']}")
                    st.write(f"**Duración total:** {proc['duracion']}")
                    st.write(f"**Tiempo de espera:** {proc['espera']}")
                    st.write(f"**Tiempo de retorno:** {proc['retorno']}")
                    st.write("**Segmentos de ejecución:**", proc['ejecuciones'])
    else:
        st.error("❌ Por favor ingresa al menos un proceso")

# Información adicional
with st.expander("📚 Explicación del Algoritmo SRT"):
    st.markdown("""
    **Cómo funciona SRT:**
    
    1. **Preemptivo**: Puede interrumpir procesos en ejecución
    2. **Selección**: Siempre elige el proceso con menor tiempo restante
    3. **Respuesta**: Excelente para tiempos de respuesta cortos
    4. **Cola de preparados**: Se reevalúa en cada interrupción/llegada
    
    **Ventajas:**
    - Minimiza el tiempo de respuesta promedio
    - Eficiente para cargas de trabajo mixtas
    - Mejor que SJF en términos de respuesta
    
    **Desventajas:**
    - Posibilidad de inanición para procesos largos
    - Overhead por cambios de contexto
    - Complejidad de implementación
    """)