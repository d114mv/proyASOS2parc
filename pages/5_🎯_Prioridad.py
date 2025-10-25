import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.prioridad import calcular_prioridad
from utils.visualizacion import crear_grafico_gantt, mostrar_metricas
from utils.helpers import validar_procesos, calcular_tiempo_total

st.set_page_config(
    page_title="Prioridad - Simulador Planificación",
    page_icon="🎯",
    layout="wide"
)

if 'procesos_pri' not in st.session_state:
    st.session_state.procesos_pri = []
if 'procesos_calculados_pri' not in st.session_state:
    st.session_state.procesos_calculados_pri = []
if 'tiempo_actual_pri' not in st.session_state:
    st.session_state.tiempo_actual_pri = 0
if 'simulacion_iniciada_pri' not in st.session_state:
    st.session_state.simulacion_iniciada_pri = False

def main():
    st.title("🎯 Planificación por Prioridad")
    
    st.markdown("""
    El algoritmo de **Planificación por Prioridad** ejecuta procesos basado en niveles 
    de prioridad asignados. Menor número = mayor prioridad (0 es la más alta).
    """)
    
    with st.sidebar:
        st.header("ℹ️ Acerca de Prioridad")
        st.info("""
        **Características:**
        - ⚡ Puede ser preemptivo o no
        - ✅ Flexible para diferentes necesidades
        - ❌ Inanición para prioridades bajas
        - ❌ Requiere definir prioridades
        - ⚠️ Puede ser injusto
        """)
        
        st.header("🎯 Escala de Prioridad")
        st.metric("0", "Máxima prioridad", delta="Alta")
        st.metric("5", "Prioridad media", delta="Media") 
        st.metric("10", "Mínima prioridad", delta="Baja")
        
        if st.button("🏠 Volver al Inicio"):
            st.switch_page("app.py")
    
    st.header("📥 Configuración de Procesos")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        num_procesos = st.number_input(
            "Número de procesos",
            min_value=1,
            max_value=8,
            value=4,
            key="pri_procesos"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔄 Reiniciar Procesos", use_container_width=True):
            st.session_state.procesos_pri = []
            st.session_state.simulacion_iniciada_pri = False
            st.rerun()
    
    st.subheader("✏️ Definir Procesos y Prioridades")
    
    st.info("💡 **Recordatorio:** Menor número = Mayor prioridad (0 es la más alta)")
    
    if not st.session_state.procesos_pri:
        st.session_state.procesos_pri = [
            {'pid': i, 'llegada': 0, 'duracion': (i+1)*2, 'prioridad': i} 
            for i in range(num_procesos)
        ]
    
    procesos_pri = []
    for i in range(num_procesos):
        col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
        with col1:
            st.write(f"**Proceso {i}**")
        with col2:
            llegada = st.number_input(
                f"Llegada P{i}",
                min_value=0,
                value=st.session_state.procesos_pri[i]['llegada'] if i < len(st.session_state.procesos_pri) else 0,
                key=f"llegada_pri_{i}"
            )
        with col3:
            duracion = st.number_input(
                f"Duración P{i}",
                min_value=1,
                value=st.session_state.procesos_pri[i]['duracion'] if i < len(st.session_state.procesos_pri) else (i+1)*2,
                key=f"duracion_pri_{i}"
            )
        with col4:
            prioridad = st.number_input(
                f"Prioridad P{i}",
                min_value=0,
                max_value=10,
                value=st.session_state.procesos_pri[i]['prioridad'] if i < len(st.session_state.procesos_pri) else i,
                help="0 = Máxima prioridad, 10 = Mínima prioridad",
                key=f"prioridad_pri_{i}"
            )
        
        procesos_pri.append({
            'pid': i,
            'llegada': llegada,
            'duracion': duracion,
            'prioridad': prioridad
        })
    
    st.session_state.procesos_pri = procesos_pri
    
    if st.session_state.procesos_pri:
        st.subheader("📋 Procesos (Ordenados por Prioridad)")
        procesos_ordenados = sorted(st.session_state.procesos_pri, key=lambda x: x['prioridad'])
        df_pri = pd.DataFrame(procesos_ordenados)
        df_pri['Proceso'] = df_pri['pid'].apply(lambda x: f'P{x}')
        df_pri['Nivel Prioridad'] = df_pri['prioridad'].apply(
            lambda x: "🔥 Máxima" if x == 0 else "✅ Alta" if x <= 3 else "⚠️ Media" if x <= 6 else "🔻 Baja"
        )
        df_pri['Orden Ejecución'] = range(1, len(procesos_ordenados) + 1)
        st.dataframe(df_pri[['Orden Ejecución', 'Proceso', 'Nivel Prioridad', 'prioridad', 'llegada', 'duracion']], 
                    use_container_width=True)
    
    st.header("🎯 Simulación por Prioridad")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🚀 Ejecutar Simulación Prioridad", type="primary", use_container_width=True):
            es_valido, mensaje = validar_procesos(st.session_state.procesos_pri)
            if es_valido:
                with st.spinner("Calculando planificación por prioridad..."):
                    procesos_calculados = calcular_prioridad(st.session_state.procesos_pri.copy())
                    
                    st.session_state.procesos_calculados_pri = procesos_calculados
                    st.session_state.tiempo_actual_pri = 0
                    st.session_state.simulacion_iniciada_pri = True
                    st.rerun()
            else:
                st.error(f"❌ {mensaje}")
    
    with col2:
        if st.button("🔄 Reiniciar Simulación", use_container_width=True):
            st.session_state.simulacion_iniciada_pri = False
            st.session_state.tiempo_actual_pri = 0
            st.rerun()
    
    if st.session_state.get("simulacion_iniciada_pri", False):
        st.header("📊 Resultados de la Simulación por Prioridad")
        
        tiempo_actual = st.session_state.tiempo_actual_pri
        tiempo_total = calcular_tiempo_total(st.session_state.procesos_calculados_pri)
        
        st.subheader(f"⏰ Tiempo Actual: {tiempo_actual} / {tiempo_total}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⏮️ Reiniciar", key="reiniciar_pri", use_container_width=True):
                st.session_state.tiempo_actual_pri = 0
                st.rerun()
        
        with col2:
            if st.button("◀️ Retroceder", key="retroceder_pri", use_container_width=True):
                if st.session_state.tiempo_actual_pri > 0:
                    st.session_state.tiempo_actual_pri -= 1
                    st.rerun()
        
        with col3:
            if st.button("Avanzar ▶️", key="avanzar_pri", use_container_width=True):
                if st.session_state.tiempo_actual_pri < tiempo_total:
                    st.session_state.tiempo_actual_pri += 1
                    st.rerun()
        
        with col4:
            if st.button("▶️▶️ Ver Todo", key="vertodo_pri", use_container_width=True):
                st.session_state.tiempo_actual_pri = tiempo_total
                st.rerun()
        
        if tiempo_total > 0:
            st.progress(st.session_state.tiempo_actual_pri / tiempo_total)
        else:
            st.progress(0)
        
        fig = crear_grafico_gantt(
            st.session_state.procesos_calculados_pri,
            st.session_state.tiempo_actual_pri,
            "Prioridad"
        )
        st.pyplot(fig)
        
        if st.session_state.tiempo_actual_pri == tiempo_total:
            st.markdown("---")
            st.subheader("📈 Métricas Finales por Prioridad")
            
            metricas = mostrar_metricas(st.session_state.procesos_calculados_pri)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⏱️ Retorno Promedio", f"{metricas['retorno_promedio']:.2f}")
            with col2:
                st.metric("⏳ Espera Promedio", f"{metricas['espera_promedio']:.2f}")
            with col3:
                st.metric("✅ Procesos Completados", metricas['procesos_completados'])
            
            st.subheader("🎯 Análisis por Niveles de Prioridad")
            
            df_analisis = pd.DataFrame(st.session_state.procesos_calculados_pri)
            df_analisis['Nivel'] = df_analisis['prioridad'].apply(
                lambda x: "Alta" if x <= 3 else "Media" if x <= 6 else "Baja"
            )
            
            stats_prioridad = df_analisis.groupby('Nivel').agg({
                'retorno': 'mean',
                'espera': 'mean',
                'pid': 'count'
            }).round(2)
            
            stats_prioridad.columns = ['Retorno Promedio', 'Espera Promedio', 'Cantidad Procesos']
            st.dataframe(stats_prioridad, use_container_width=True)
            
            st.subheader("🔄 Secuencia de Ejecución")
            secuencia = " → ".join([f"P{p['pid']}({p['prioridad']})" for p in st.session_state.procesos_calculados_pri])
            st.success(f"**Orden de ejecución:** {secuencia}")
        
        with st.expander("📋 Ver detalles de procesos calculados"):
            st.dataframe(pd.DataFrame(st.session_state.procesos_calculados_pri))
    
    with st.expander("📚 Explicación Detallada del Algoritmo de Prioridad"):
        st.markdown("""
        ## 🎯 Planificación por Prioridad
        
        **¿Cómo funciona?**
        
        La planificación por prioridad asigna un nivel de prioridad a cada proceso:
        
        1. **Se ejecuta el proceso** con mayor prioridad (menor número)
        2. **Si hay empate**, puede usar FCFS como desempate
        3. **Versión no preemptiva:** Una vez que comienza, ejecuta hasta terminar
        4. **Versión preemptiva:** Si llega uno con mayor prioridad, interrumpe el actual
        
        **Ejemplo práctico (no preemptivo):**
        ```
        Procesos: P0(prioridad=2), P1(prioridad=0), P2(prioridad=1), P3(prioridad=2)
        
        Orden por prioridad: P1(0) → P2(1) → P0(2) → P3(2)
        
        Tiempo 0: Ejecuta P1 (prioridad 0 - más alta)
        Tiempo X: P1 termina, ejecuta P2 (siguiente más alta)
        Tiempo Y: P2 termina, ejecuta P0 (empate con P3, orden llegada)
        Tiempo Z: P0 termina, ejecuta P3
        ```
        
        **Sistemas de prioridad comunes:**
        - **Numérico:** 0 (máxima) a N (mínima)
        - **Linux nice:** -20 (máxima) a +19 (mínima)  
        - **Windows:** 6 niveles (Idle, Normal, High, etc.)
        
        **Ventajas:**
        - ✅ **Flexible** - puede adaptarse a diferentes necesidades
        - ✅ **Importancia real** - procesos críticos se ejecutan primero
        - ✅ **Puede combinarse** con otros algoritmos
        - ✅ **Adecuado para sistemas en tiempo real**
        
        **Desventajas:**
        - ❌ **Inanición** - procesos de baja prioridad pueden nunca ejecutar
        - ❌ **Subjetivo** - definir prioridades puede ser difícil
        - ❌ **Puede ser injusto** - ignora equidad
        - ❌ **Overhead** - gestión de colas por prioridad
        
        **Soluciones para inanición:**
        - **Aging:** Aumentar prioridad de procesos que esperan mucho tiempo
        - **Lotes por prioridad:** Agrupar procesos similares
        - **Límites de tiempo:** Máximo tiempo de ejecución por prioridad
        
        **Aplicaciones en la vida real:**
        - Sistemas en tiempo real (RTOS)
        - Procesos del sistema vs procesos de usuario
        - Aplicaciones críticas (servicios de red, E/S)
        - Videojuegos (procesos de renderizado alta prioridad)
        
        **Consejo:** Combinar con aging evita la inanición y hace el sistema más justo.
        """)

if __name__ == "__main__":
    main()