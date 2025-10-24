import streamlit as st
import pandas as pd
import sys
import os

# Agregar utils al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.fcfs import calcular_fcfs
from utils.visualizacion import crear_grafico_gantt, mostrar_metricas
from utils.helpers import validar_procesos, calcular_tiempo_total

st.set_page_config(
    page_title="FCFS - Simulador Planificación",
    page_icon="⚙️",
    layout="wide"
)

# Inicializar session state
if 'procesos_fcfs' not in st.session_state:
    st.session_state.procesos_fcfs = []
if 'procesos_calculados_fcfs' not in st.session_state:
    st.session_state.procesos_calculados_fcfs = []
if 'tiempo_actual_fcfs' not in st.session_state:
    st.session_state.tiempo_actual_fcfs = 0
if 'simulacion_iniciada_fcfs' not in st.session_state:
    st.session_state.simulacion_iniciada_fcfs = False

def main():
    st.title("⚙️ Algoritmo FCFS (First Come First Served)")
    
    st.markdown("""
    El algoritmo **FCFS (First Come First Served)** es el más simple de planificación. 
    Los procesos se ejecutan en el orden exacto en que llegan, sin prioridades ni interrupciones.
    """)
    
    # Sidebar con información
    with st.sidebar:
        st.header("ℹ️ Acerca de FCFS")
        st.info("""
        **Características:**
        - ❌ No preemptivo
        - ✅ Simple de implementar
        - ✅ Justo en orden de llegada
        - ❌ Efecto convoy
        - ❌ Poco responsivo
        """)
        
        st.header("📊 Métricas Clave")
        st.metric("Complejidad", "O(n)")
        st.metric("Preemptivo", "No")
        st.metric("Óptimo para", "Procesos similares")
        
        if st.button("🏠 Volver al Inicio"):
            st.switch_page("app.py")
    
    # Entrada de datos
    st.header("📥 Configuración de Procesos")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        num_procesos = st.number_input(
            "Número de procesos",
            min_value=1,
            max_value=10,
            value=4,
            key="num_fcfs"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔄 Reiniciar Procesos", use_container_width=True):
            st.session_state.procesos_fcfs = []
            st.session_state.simulacion_iniciada_fcfs = False
            st.rerun()
    
    # Formulario para procesos
    st.subheader("✏️ Definir Procesos FCFS")
    
    if not st.session_state.procesos_fcfs:
        # Inicializar procesos por defecto
        st.session_state.procesos_fcfs = [
            {'pid': i, 'llegada': i, 'duracion': (i+1)*2} 
            for i in range(num_procesos)
        ]
    
    # Editor de datos
    datos_procesos = []
    for i in range(num_procesos):
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.write(f"**Proceso {i}**")
        with col2:
            llegada = st.number_input(
                f"Llegada P{i}",
                min_value=0,
                value=st.session_state.procesos_fcfs[i]['llegada'] if i < len(st.session_state.procesos_fcfs) else i,
                key=f"llegada_fcfs_{i}"
            )
        with col3:
            duracion = st.number_input(
                f"Duración P{i}",
                min_value=1,
                value=st.session_state.procesos_fcfs[i]['duracion'] if i < len(st.session_state.procesos_fcfs) else (i+1)*2,
                key=f"duracion_fcfs_{i}"
            )
        
        datos_procesos.append({
            'pid': i,
            'llegada': llegada,
            'duracion': duracion
        })
    
    st.session_state.procesos_fcfs = datos_procesos
    
    # Mostrar resumen
    if st.session_state.procesos_fcfs:
        st.subheader("📋 Procesos Configurados")
        df_procesos = pd.DataFrame(st.session_state.procesos_fcfs)
        df_procesos['Proceso'] = df_procesos['pid'].apply(lambda x: f'P{x}')
        df_procesos['Orden Llegada'] = df_procesos['llegada'].rank(method='dense').astype(int)
        st.dataframe(df_procesos[['Proceso', 'Orden Llegada', 'llegada', 'duracion']], use_container_width=True)
    
    # Ejecutar simulación
    st.header("🎯 Simulación FCFS")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🚀 Ejecutar Simulación FCFS", type="primary", use_container_width=True):
            # Validar procesos
            es_valido, mensaje = validar_procesos(st.session_state.procesos_fcfs)
            if es_valido:
                with st.spinner("Calculando planificación FCFS..."):
                    # Calcular FCFS
                    procesos_calculados = calcular_fcfs(st.session_state.procesos_fcfs.copy())
                    
                    # Guardar resultados
                    st.session_state.procesos_calculados_fcfs = procesos_calculados
                    st.session_state.tiempo_actual_fcfs = 0
                    st.session_state.simulacion_iniciada_fcfs = True
                    st.rerun()
            else:
                st.error(f"❌ {mensaje}")
    
    with col2:
        if st.button("🔄 Reiniciar Simulación", use_container_width=True):
            st.session_state.simulacion_iniciada_fcfs = False
            st.session_state.tiempo_actual_fcfs = 0
            st.rerun()
    
    # Visualización de resultados
    if st.session_state.get("simulacion_iniciada_fcfs", False):
        st.header("📊 Resultados de la Simulación FCFS")
        
        tiempo_actual = st.session_state.tiempo_actual_fcfs
        tiempo_total = calcular_tiempo_total(st.session_state.procesos_calculados_fcfs)
        
        # Controles de simulación
        st.subheader(f"⏰ Tiempo Actual: {tiempo_actual} / {tiempo_total}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⏮️ Reiniciar", key="reiniciar_fcfs", use_container_width=True):
                st.session_state.tiempo_actual_fcfs = 0
                st.rerun()
        
        with col2:
            if st.button("◀️ Retroceder", key="retroceder_fcfs", use_container_width=True):
                if st.session_state.tiempo_actual_fcfs > 0:
                    st.session_state.tiempo_actual_fcfs -= 1
                    st.rerun()
        
        with col3:
            if st.button("Avanzar ▶️", key="avanzar_fcfs", use_container_width=True):
                if st.session_state.tiempo_actual_fcfs < tiempo_total:
                    st.session_state.tiempo_actual_fcfs += 1
                    st.rerun()
        
        with col4:
            if st.button("▶️▶️ Ver Todo", key="vertodo_fcfs", use_container_width=True):
                st.session_state.tiempo_actual_fcfs = tiempo_total
                st.rerun()
        
        # Barra de progreso
        if tiempo_total > 0:
            st.progress(st.session_state.tiempo_actual_fcfs / tiempo_total)
        else:
            st.progress(0)
        
        # Gráfico de Gantt
        fig = crear_grafico_gantt(
            st.session_state.procesos_calculados_fcfs,
            st.session_state.tiempo_actual_fcfs,
            "FCFS"
        )
        st.pyplot(fig)
        
        # Métricas cuando termine la simulación
        if st.session_state.tiempo_actual_fcfs == tiempo_total:
            st.markdown("---")
            st.subheader("📈 Métricas Finales FCFS")
            
            metricas = mostrar_metricas(st.session_state.procesos_calculados_fcfs)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⏱️ Retorno Promedio", f"{metricas['retorno_promedio']:.2f}")
            with col2:
                st.metric("⏳ Espera Promedio", f"{metricas['espera_promedio']:.2f}")
            with col3:
                st.metric("✅ Procesos Completados", metricas['procesos_completados'])
            
            # Secuencia de ejecución
            st.subheader("🔄 Secuencia de Ejecución")
            secuencia = " → ".join([f"P{p['pid']}" for p in st.session_state.procesos_calculados_fcfs])
            st.success(f"**Orden de ejecución:** {secuencia}")
        
        # Tabla detallada
        with st.expander("📋 Ver detalles de procesos calculados"):
            st.dataframe(pd.DataFrame(st.session_state.procesos_calculados_fcfs))
    
    # Información educativa
    with st.expander("📚 Explicación Detallada del Algoritmo FCFS"):
        st.markdown("""
        ## ⚙️ First Come First Served (FCFS)
        
        **¿Cómo funciona?**
        
        FCFS es el algoritmo de planificación más simple:
        
        1. **Los procesos se ejecutan** en el orden exacto de su llegada
        2. **No hay interrupciones** - una vez que un proceso comienza, ejecuta hasta completar
        3. **La cola de listos** es una simple cola FIFO (First In, First Out)
        
        **Ejemplo práctico:**
        ```
        Procesos: P0(llegada=0, duración=5), P1(llegada=1, duración=3), P2(llegada=2, duración=8)
        
        Tiempo 0: Ejecuta P0 (llega primero)
        Tiempo 5: P0 termina, ejecuta P1 (siguiente en cola)  
        Tiempo 8: P1 termina, ejecuta P2 (último en llegar)
        Tiempo 16: P2 termina
        ```
        
        **Ventajas:**
        - ✅ Extremadamente simple de implementar
        - ✅ Justo en términos de orden de llegada
        - ✅ Bajo overhead del sistema
        - ✅ Predecible y fácil de entender
        
        **Desventajas:**
        - ❌ **Efecto convoy**: Procesos largos retrasan a los cortos
        - ❌ **Poco responsivo**: Procesos urgentes deben esperar
        - ❌ **Bajo rendimiento** en términos de tiempo de espera promedio
        - ❌ **No adecuado** para sistemas interactivos
        
        **Fórmulas importantes:**
        - **Tiempo de retorno** = Tiempo final - Tiempo de llegada
        - **Tiempo de espera** = Tiempo de retorno - Tiempo de CPU
        - **Throughput** = Número de procesos / Tiempo total
        
        **Aplicaciones en la vida real:**
        - Sistemas por lotes (batch) simples
        - Colas de impresión
        - Procesamiento offline no crítico
        - Situaciones donde la simplicidad es más importante que el rendimiento
        
        **Consejo:** FCFS funciona mejor cuando todos los procesos tienen duraciones similares.
        """)

if __name__ == "__main__":
    main()