import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.sjf import calcular_sjf
from utils.visualizacion import crear_grafico_gantt, mostrar_metricas
from utils.helpers import validar_procesos, calcular_tiempo_total

st.set_page_config(
    page_title="SJF - Simulador Planificación", 
    page_icon="📊",
    layout="wide"
)

if 'procesos_sjf' not in st.session_state:
    st.session_state.procesos_sjf = []
if 'procesos_calculados_sjf' not in st.session_state:
    st.session_state.procesos_calculados_sjf = []
if 'tiempo_actual_sjf' not in st.session_state:
    st.session_state.tiempo_actual_sjf = 0
if 'simulacion_iniciada_sjf' not in st.session_state:
    st.session_state.simulacion_iniciada_sjf = False

def main():
    st.title("📊 Algoritmo SJF (Shortest Job First)")
    
    st.markdown("""
    El algoritmo **SJF (Shortest Job First)** ejecuta primero los procesos con **menor tiempo de CPU**,
    minimizando el tiempo de espera promedio. Esta versión es **no preemptiva**.
    """)
    
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
        
        st.header("📊 Métricas Clave")
        st.metric("Complejidad", "O(n log n)")
        st.metric("Preemptivo", "No")
        st.metric("Óptimo para", "Procesos conocidos")
        
        if st.button("🏠 Volver al Inicio"):
            st.switch_page("app.py")
    
    st.header("📥 Configuración de Procesos")
    
    st.info("💡 **Nota:** En SJF clásico, todos los procesos llegan al tiempo 0")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        num_procesos = st.number_input(
            "Número de procesos", 
            min_value=1, 
            max_value=8, 
            value=4,
            key="sjf_procesos"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔄 Reiniciar Procesos", use_container_width=True):
            st.session_state.procesos_sjf = []
            st.session_state.simulacion_iniciada_sjf = False
            st.rerun()
    
    st.subheader("✏️ Definir Duraciones de Procesos")
    
    if not st.session_state.procesos_sjf:
        st.session_state.procesos_sjf = [
            {'pid': i, 'llegada': 0, 'duracion': (i+1)*2} 
            for i in range(num_procesos)
        ]
    
    procesos_sjf = []
    cols = st.columns(4)
    
    for i in range(num_procesos):
        with cols[i % 4]:
            duracion = st.number_input(
                f"Duración P{i}", 
                min_value=1, 
                value=st.session_state.procesos_sjf[i]['duracion'] if i < len(st.session_state.procesos_sjf) else (i+1)*2,
                key=f"sjf_duracion_{i}"
            )
            
            procesos_sjf.append({
                'pid': i,
                'llegada': 0,
                'duracion': duracion
            })
    
    st.session_state.procesos_sjf = procesos_sjf
    
    if st.session_state.procesos_sjf:
        st.subheader("📋 Procesos (Ordenados por Duración)")
        procesos_ordenados = sorted(st.session_state.procesos_sjf, key=lambda x: x['duracion'])
        df_sjf = pd.DataFrame(procesos_ordenados)
        df_sjf['Proceso'] = df_sjf['pid'].apply(lambda x: f'P{x}')
        df_sjf['Orden Ejecución'] = range(1, len(procesos_ordenados) + 1)
        st.dataframe(df_sjf[['Orden Ejecución', 'Proceso', 'duracion']], use_container_width=True)
    
    st.header("🎯 Simulación SJF")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🚀 Ejecutar Simulación SJF", type="primary", use_container_width=True):
            es_valido, mensaje = validar_procesos(st.session_state.procesos_sjf)
            if es_valido:
                with st.spinner("Ejecutando algoritmo SJF..."):
                    resultado_sjf = calcular_sjf(st.session_state.procesos_sjf.copy())
                    
                    st.session_state.procesos_calculados_sjf = resultado_sjf
                    st.session_state.tiempo_total_sjf = calcular_tiempo_total(resultado_sjf)
                    st.session_state.tiempo_actual_sjf = 0
                    st.session_state.simulacion_iniciada_sjf = True
                    st.rerun()
            else:
                st.error(f"❌ {mensaje}")
    
    with col2:
        if st.button("🔄 Reiniciar Simulación", use_container_width=True):
            st.session_state.simulacion_iniciada_sjf = False
            st.session_state.tiempo_actual_sjf = 0
            st.rerun()
    
    if st.session_state.get("simulacion_iniciada_sjf", False):
        st.header("📊 Visualización de la Simulación SJF")
        
        tiempo_actual = st.session_state.tiempo_actual_sjf
        tiempo_total = st.session_state.tiempo_total_sjf
        
        st.subheader(f"⏰ Tiempo Actual: {tiempo_actual} / {tiempo_total}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        if col1.button("⏮️ Reiniciar", key="reiniciar_sjf"):
            st.session_state.tiempo_actual_sjf = 0
            st.rerun()

        if col2.button("◀️ Retroceder", key="retroceder_sjf"):
            if st.session_state.tiempo_actual_sjf > 0:
                st.session_state.tiempo_actual_sjf -= 1
                st.rerun()

        if col3.button("Avanzar ▶️", key="avanzar_sjf"):
            if st.session_state.tiempo_actual_sjf < tiempo_total:
                st.session_state.tiempo_actual_sjf += 1
                st.rerun()

        if col4.button("▶️▶️ Ver Todo", key="ver_todo_sjf"):
            st.session_state.tiempo_actual_sjf = tiempo_total
            st.rerun()

        if tiempo_total > 0:
            st.progress(st.session_state.tiempo_actual_sjf / tiempo_total)
        else:
            st.progress(0)

        fig = crear_grafico_gantt(
            st.session_state.procesos_calculados_sjf,
            st.session_state.tiempo_actual_sjf,
            "SJF"
        )
        
        st.pyplot(fig)

        if st.session_state.tiempo_actual_sjf == tiempo_total:
            st.markdown("---")
            st.subheader("📈 Métricas Finales SJF")
            
            metricas = mostrar_metricas(st.session_state.procesos_calculados_sjf)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⏱️ Retorno Promedio", f"{metricas['retorno_promedio']:.2f}")
            with col2:
                st.metric("⏳ Espera Promedio", f"{metricas['espera_promedio']:.2f}")
            with col3:
                st.metric("✅ Procesos Completados", metricas['procesos_completados'])
            
            st.subheader("🔄 Secuencia de Ejecución")
            secuencia = " → ".join([f"P{p['pid']}" for p in st.session_state.procesos_calculados_sjf])
            st.success(f"**Orden de ejecución:** {secuencia}")

        with st.expander("📋 Ver datos calculados de los procesos"):
            st.dataframe(pd.DataFrame(st.session_state.procesos_calculados_sjf))

    with st.expander("📚 Explicación del Algoritmo SJF"):
        st.markdown("""
        ## 📊 Shortest Job First (SJF)
        
        **¿Cómo funciona SJF (No Preemptivo)?**
        
        1. **Todos los procesos** llegan al tiempo 0 (asumido)
        2. **Se ordenan** por duración de CPU (menor a mayor)
        3. **Se ejecutan** en ese orden hasta completar
        4. **No hay interrupciones** una vez que empieza un proceso
        
        **Ejemplo práctico:**
        ```
        Procesos: P0(duración=8), P1(duración=4), P2(duración=2), P3(duración=6)
        
        Orden SJF: P2 → P1 → P3 → P0  (por duración: 2, 4, 6, 8)
        
        Tiempo 0: Ejecuta P2 (más corto)
        Tiempo 2: P2 termina, ejecuta P1 (siguiente más corto)
        Tiempo 6: P1 termina, ejecuta P3 
        Tiempo 12: P3 termina, ejecuta P0
        Tiempo 20: P0 termina
        ```
        
        **Ventajas:**
        - ✅ **Mínimo tiempo de espera promedio** posible para lotes
        - ✅ Simple de entender e implementar
        - ✅ Eficiente para procesos por lotes
        - ✅ Mejor que FCFS en términos de rendimiento
        
        **Desventajas:**
        - ❌ **Inanición** para procesos largos
        - ❌ **Requiere conocer duraciones** de antemano
        - ❌ **No es preemptivo** (poco responsivo)
        - ❌ **Impráctico** en sistemas interactivos
        
        **Variante preemptiva: SRT**
        - SJF puede hacerse preemptivo (SRT - Shortest Remaining Time)
        - En SRT, si llega un proceso más corto, interrumpe el actual
        
        **Fórmula de optimalidad:**
        - SJF es **óptimo** para minimizar el tiempo de espera promedio
        - Pero solo cuando todos los procesos están disponibles al mismo tiempo
        
        **Aplicaciones en la vida real:**
        - Procesamiento por lotes (batch processing)
        - Sistemas de backend con trabajos conocidos
        - Renderizado de video/audio con duraciones estimadas
        - Compilación de proyectos grandes
        
        **Consejo:** SJF funciona mejor cuando las duraciones son conocidas y hay mezcla de procesos cortos y largos.
        """)

if __name__ == "__main__":
    main()