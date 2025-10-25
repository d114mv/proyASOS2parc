import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.srt import calcular_srt
from utils.visualizacion import crear_grafico_gantt, mostrar_metricas
from utils.helpers import validar_procesos, calcular_tiempo_total

st.set_page_config(
    page_title="SRT - Simulador Planificación",
    page_icon="⚡",
    layout="wide"
)

if 'procesos_srt' not in st.session_state:
    st.session_state.procesos_srt = []
if 'procesos_calculados_srt' not in st.session_state:
    st.session_state.procesos_calculados_srt = []
if 'tiempo_actual_srt' not in st.session_state:
    st.session_state.tiempo_actual_srt = 0
if 'simulacion_iniciada_srt' not in st.session_state:
    st.session_state.simulacion_iniciada_srt = False

def main():
    st.title("⚡ Algoritmo SRT (Shortest Remaining Time)")
    
    st.markdown("""
    El algoritmo **SRT (Shortest Remaining Time)** es la versión preemptiva de SJF. 
    Siempre ejecuta el proceso con **menor tiempo restante de ejecución**, proporcionando 
    los mejores tiempos de respuesta para procesos cortos.
    """)
    
    with st.sidebar:
        st.header("ℹ️ Acerca de SRT")
        st.info("""
        **Características:**
        - ✅ Preemptivo
        - ✅ Excelente tiempo de respuesta
        - ✅ Minimiza tiempo de espera
        - ❌ Inanición para procesos largos
        - ❌ Alto overhead por cambios
        """)
        
        st.header("📊 Métricas Clave")
        st.metric("Complejidad", "O(n log n)")
        st.metric("Preemptivo", "Sí")
        st.metric("Óptimo para", "Procesos cortos")
        
        if st.button("🏠 Volver al Inicio"):
            st.switch_page("app.py")
    
    st.header("📥 Configuración de Procesos")
    
    st.info("💡 **SRT es preemptivo:** Los procesos pueden interrumpirse si llega uno más corto")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        num_procesos = st.number_input(
            "Número de procesos",
            min_value=1,
            max_value=8,
            value=4,
            key="srt_procesos"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔄 Reiniciar Procesos", use_container_width=True):
            st.session_state.procesos_srt = []
            st.session_state.simulacion_iniciada_srt = False
            st.rerun()
    
    st.subheader("✏️ Definir Procesos SRT")
    
    if not st.session_state.procesos_srt:
        st.session_state.procesos_srt = [
            {'pid': i, 'llegada': i, 'duracion': (i+1)*2} 
            for i in range(num_procesos)
        ]
    
    procesos_srt = []
    for i in range(num_procesos):
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.write(f"**Proceso {i}**")
        with col2:
            llegada = st.number_input(
                f"Llegada P{i}",
                min_value=0,
                value=st.session_state.procesos_srt[i]['llegada'] if i < len(st.session_state.procesos_srt) else i,
                key=f"llegada_srt_{i}"
            )
        with col3:
            duracion = st.number_input(
                f"Duración P{i}",
                min_value=1,
                value=st.session_state.procesos_srt[i]['duracion'] if i < len(st.session_state.procesos_srt) else (i+1)*2,
                key=f"duracion_srt_{i}"
            )
        
        procesos_srt.append({
            'pid': i,
            'llegada': llegada,
            'duracion': duracion
        })
    
    st.session_state.procesos_srt = procesos_srt
    
    if st.session_state.procesos_srt:
        st.subheader("📋 Procesos Configurados")
        df_procesos = pd.DataFrame(st.session_state.procesos_srt)
        df_procesos['Proceso'] = df_procesos['pid'].apply(lambda x: f'P{x}')
        df_procesos['Tiempo Restante Inicial'] = df_procesos['duracion']
        st.dataframe(df_procesos[['Proceso', 'llegada', 'duracion', 'Tiempo Restante Inicial']], 
                    use_container_width=True)
    
    st.header("🎯 Simulación SRT")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🚀 Ejecutar Simulación SRT", type="primary", use_container_width=True):
            es_valido, mensaje = validar_procesos(st.session_state.procesos_srt)
            if es_valido:
                with st.spinner("Calculando planificación SRT..."):
                    procesos_calculados = calcular_srt(st.session_state.procesos_srt.copy())
                    
                    st.session_state.procesos_calculados_srt = procesos_calculados
                    st.session_state.tiempo_actual_srt = 0
                    st.session_state.simulacion_iniciada_srt = True
                    st.rerun()
            else:
                st.error(f"❌ {mensaje}")
    
    with col2:
        if st.button("🔄 Reiniciar Simulación", use_container_width=True):
            st.session_state.simulacion_iniciada_srt = False
            st.session_state.tiempo_actual_srt = 0
            st.rerun()
    
    if st.session_state.get("simulacion_iniciada_srt", False):
        st.header("📊 Resultados de la Simulación SRT")
        
        tiempo_actual = st.session_state.tiempo_actual_srt
        tiempo_total = calcular_tiempo_total(st.session_state.procesos_calculados_srt)
        
        st.subheader(f"⏰ Tiempo Actual: {tiempo_actual} / {tiempo_total}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⏮️ Reiniciar", key="reiniciar_srt", use_container_width=True):
                st.session_state.tiempo_actual_srt = 0
                st.rerun()
        
        with col2:
            if st.button("◀️ Retroceder", key="retroceder_srt", use_container_width=True):
                if st.session_state.tiempo_actual_srt > 0:
                    st.session_state.tiempo_actual_srt -= 1
                    st.rerun()
        
        with col3:
            if st.button("Avanzar ▶️", key="avanzar_srt", use_container_width=True):
                if st.session_state.tiempo_actual_srt < tiempo_total:
                    st.session_state.tiempo_actual_srt += 1
                    st.rerun()
        
        with col4:
            if st.button("▶️▶️ Ver Todo", key="vertodo_srt", use_container_width=True):
                st.session_state.tiempo_actual_srt = tiempo_total
                st.rerun()
        
        if tiempo_total > 0:
            st.progress(st.session_state.tiempo_actual_srt / tiempo_total)
        else:
            st.progress(0)
        
        fig = crear_grafico_gantt(
            st.session_state.procesos_calculados_srt,
            st.session_state.tiempo_actual_srt,
            "SRT"
        )
        st.pyplot(fig)
        
        if st.session_state.tiempo_actual_srt == tiempo_total:
            st.markdown("---")
            st.subheader("📈 Métricas Finales SRT")
            
            metricas = mostrar_metricas(st.session_state.procesos_calculados_srt)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⏱️ Retorno Promedio", f"{metricas['retorno_promedio']:.2f}")
            with col2:
                st.metric("⏳ Espera Promedio", f"{metricas['espera_promedio']:.2f}")
            with col3:
                st.metric("✅ Procesos Completados", metricas['procesos_completados'])
            
            st.subheader("🔁 Análisis de Preempciones SRT")
            
            total_preempciones = 0
            for proceso in st.session_state.procesos_calculados_srt:
                if 'ejecuciones' in proceso and len(proceso['ejecuciones']) > 1:
                    total_preempciones += len(proceso['ejecuciones']) - 1
            
            st.info(f"**Total de preempciones:** {total_preempciones} cambios entre procesos")
            
            with st.expander("🔍 Ver detalles de ejecuciones por proceso"):
                for proceso in st.session_state.procesos_calculados_srt:
                    if 'ejecuciones' in proceso:
                        ejecuciones_str = " + ".join([f"{dur}t@T{ini}" for ini, dur in proceso['ejecuciones']])
                        st.write(f"**P{proceso['pid']}:** {ejecuciones_str} = {proceso['duracion']}t total")
        
        with st.expander("📋 Ver detalles de procesos calculados"):
            st.dataframe(pd.DataFrame(st.session_state.procesos_calculados_srt))
    
    with st.expander("📚 Explicación Detallada del Algoritmo SRT"):
        st.markdown("""
        ## ⚡ Shortest Remaining Time (SRT)
        
        **¿Cómo funciona?**
        
        SRT es un algoritmo preemptivo que:
        
        1. **En cada unidad de tiempo**, verifica todos los procesos disponibles
        2. **Selecciona el proceso** con menor tiempo restante de ejecución
        3. **Ejecuta por 1 tick** y actualiza tiempos restantes
        4. **Si llega un proceso más corto**, puede interrumpir el actual
        5. **Repite** hasta que todos los procesos terminen
        
        **Ejemplo práctico:**
        ```
        Procesos: P0(llegada=0, duración=8), P1(llegada=1, duración=4), P2(llegada=2, duración=2)
        
        Tiempo 0: Solo P0 disponible → Ejecuta P0 (restante: 7)
        Tiempo 1: Llega P1(4) vs P0(7) → P1 más corto → Ejecuta P1 (restante: 3)  
        Tiempo 2: Llega P2(2) vs P1(3) → P2 más corto → Ejecuta P2 (restante: 1)
        Tiempo 3: P2(1) vs P1(3) → P2 más corto → Ejecuta P2 (completo)
        Tiempo 4: P1(3) vs P0(7) → P1 más corto → Ejecuta P1 (restante: 2)
        Tiempo 5: Continúa P1 (restante: 1)
        Tiempo 6: P1 completo, ejecuta P0 (restante: 6)
        ...continúa hasta que P0 termine
        ```
        
        **Ventajas:**
        - ✅ **Tiempos de respuesta mínimos** para procesos cortos
        - ✅ **Más justo que SJF** para procesos que llegan en diferentes momentos
        - ✅ **Óptimo** para minimizar tiempo de espera promedio
        - ✅ **Excelente** para sistemas interactivos
        
        **Desventajas:**
        - ❌ **Alto overhead** por cambios de contexto frecuentes
        - ❌ **Inanición** posible para procesos largos
        - ❌ **Requiere estimar** tiempos de ejecución
        - ❌ **Complejo de implementar**
        
        **Comparación con SJF:**
        - **SRT** es preemptivo, **SJF** no preemptivo
        - **SRT** mejor para procesos que llegan en diferentes momentos
        - **SJF** más simple y con menos overhead
        - **SRT** proporciona mejores tiempos de respuesta
        
        **Overhead de cambios de contexto:**
        ```
        Tiempo efectivo = Tiempo total - (Número de cambios × Duración cambio contexto)
        ```
        
        **Aplicaciones en la vida real:**
        - Sistemas interactivos de tiempo compartido
        - Servicios web con diferentes longitudes de solicitud
        - Procesamiento de transacciones con prioridad de cortos
        - Cualquier sistema donde el tiempo de respuesta es crítico
        
        **Consejo:** SRT funciona mejor cuando hay una mezcla de procesos cortos y largos, 
        y cuando se pueden estimar razonablemente las duraciones.
        """)

if __name__ == "__main__":
    main()