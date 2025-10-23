import streamlit as st
import pandas as pd
from utils.sjf import ejecutar_sjf, crear_grafico_sjf, calcular_metricas_sjf

st.set_page_config(
    page_title="SJF - Simulador Planificación", 
    page_icon="🟡",
    layout="wide"
)

st.title("🟡 Algoritmo SJF (Shortest Job First)")

st.markdown("""
El algoritmo **SJF (Shortest Job First)** ejecuta primero los procesos con **menor tiempo de CPU**,
minimizando el tiempo de espera promedio. Esta versión es **no preemptiva**.
""")

# Sidebar para información
with st.sidebar:
    st.header("ℹ️ Acerca de SJF")
    st.info("""
    **Características:**
    - ❌ No preemptivo
    - ✅ Minimiza espera promedio
    - ✅ Simple de implementar
    - ❌ Inanición posible
    - ❌ Requiere conocer duraciones
    """)
    
    if st.button("🏠 Volver al Inicio"):
        st.switch_page("app.py")

# Entrada de datos para SJF
st.header("📥 Configuración de Procesos")

st.info("💡 **Nota:** En SJF clásico, todos los procesos llegan al tiempo 0")

num_procesos_sjf = st.number_input(
    "Número de procesos", 
    min_value=1, 
    max_value=8, 
    value=4,
    key="sjf_procesos"
)

# Formulario para duraciones
st.subheader("✏️ Definir Duraciones de Procesos")

procesos_sjf = []
cols = st.columns(4)

for i in range(num_procesos_sjf):
    with cols[i % 4]:
        duracion = st.number_input(
            f"Duración P{i}", 
            min_value=1, 
            value=(i+1)*2,  # Valores por defecto variados
            key=f"sjf_duracion_{i}"
        )
        
        procesos_sjf.append({
            'pid': i,
            'duracion': duracion
        })

# Mostrar resumen
if procesos_sjf:
    st.subheader("📋 Procesos (Ordenados por Duración)")
    procesos_ordenados = sorted(procesos_sjf, key=lambda x: x['duracion'])
    df_sjf = pd.DataFrame(procesos_ordenados)
    df_sjf['Proceso'] = df_sjf['pid'].apply(lambda x: f'P{x}')
    df_sjf['Orden'] = range(1, len(procesos_ordenados) + 1)
    st.dataframe(df_sjf[['Orden', 'Proceso', 'duracion']], use_container_width=True)

# Ejecutar simulación SJF
st.header("🎯 Simulación SJF")

if st.button("🚀 Ejecutar Simulación SJF", type="primary"):
    if procesos_sjf:
        with st.spinner("Ejecutando algoritmo SJF..."):
            resultado_sjf = ejecutar_sjf(procesos_sjf)
            
            # Métricas
            col1, col2, col3 = st.columns(3)
            metricas_sjf = calcular_metricas_sjf(resultado_sjf)
            
            with col1:
                st.metric(
                    "⏱️ Tiempo de espera promedio", 
                    f"{metricas_sjf['espera_promedio']:.2f}"
                )
            
            with col2:
                st.metric(
                    "🔄 Tiempo de retorno promedio", 
                    f"{metricas_sjf['retorno_promedio']:.2f}"
                )
            
            with col3:
                st.metric(
                    "💻 Utilización de CPU", 
                    f"{metricas_sjf['utilizacion_cpu']:.1f}%"
                )
            
            # Gráfico
            st.subheader("📊 Diagrama de Gantt - SJF")
            fig_sjf = crear_grafico_sjf(resultado_sjf)
            st.pyplot(fig_sjf)
            
            # Secuencia de ejecución
            st.subheader("🔄 Secuencia de Ejecución")
            secuencia = " → ".join([f"P{p['pid']}" for p in resultado_sjf])
            st.success(f"**Orden de ejecución:** {secuencia}")
            
    else:
        st.error("❌ Por favor ingresa al menos un proceso")

# Información adicional
with st.expander("📚 Explicación del Algoritmo SJF"):
    st.markdown("""
    **Cómo funciona SJF (No Preemptivo):**
    
    1. **Todos los procesos** llegan al tiempo 0
    2. **Se ordenan** por duración de CPU (menor a mayor)
    3. **Se ejecutan** en ese orden hasta completar
    4. **No hay interrupciones** una vez que empieza un proceso
    
    **Ventajas:**
    - Mínimo tiempo de espera promedio posible
    - Simple de entender e implementar
    - Eficiente para lotes de procesos
    
    **Desventajas:**
    - Inanición para procesos largos
    - Requiere conocer duraciones de antemano
    - No es preemptivo (poco responsivo)
    
    **Óptimo para:** Procesos por lotes donde se conocen las duraciones
    """)