import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.rr import calcular_rr
from utils.visualizacion import crear_grafico_gantt, mostrar_metricas
from utils.helpers import validar_procesos, calcular_tiempo_total

st.set_page_config(
    page_title="Round Robin - Simulador Planificación",
    page_icon="🔄",
    layout="wide"
)

if 'procesos_rr' not in st.session_state:
    st.session_state.procesos_rr = []
if 'procesos_calculados_rr' not in st.session_state:
    st.session_state.procesos_calculados_rr = []
if 'tiempo_actual_rr' not in st.session_state:
    st.session_state.tiempo_actual_rr = 0
if 'simulacion_iniciada_rr' not in st.session_state:
    st.session_state.simulacion_iniciada_rr = False
if 'config_rr' not in st.session_state:
    st.session_state.config_rr = {'quantum': 3, 'cambio_contexto': 1, 'usar_cambio_contexto': False}

def main():
    st.title("🔄 Algoritmo Round Robin")
    
    st.markdown("""
    El algoritmo **Round Robin** asigna intervalos de tiempo fijos (quantum) a cada proceso,
    proporcionando un balance entre rendimiento y equidad. Es ideal para sistemas interactivos.
    """)
    
    with st.sidebar:
        st.header("ℹ️ Acerca de Round Robin")
        st.info("""
        **Características:**
        - ✅ Preemptivo
        - ✅ Justo para todos los procesos
        - ✅ Bueno para sistemas interactivos
        - ❌ Rendimiento depende del quantum
        - ❌ Overhead por cambios de contexto
        """)
        
        st.header("⚙️ Configuración Actual")
        st.metric("Quantum", st.session_state.config_rr['quantum'])
        st.metric("Cambio Contexto", 
                 f"{st.session_state.config_rr['cambio_contexto']}t" 
                 if st.session_state.config_rr['usar_cambio_contexto'] else "No")
        
        if st.button("🏠 Volver al Inicio"):
            st.switch_page("app.py")
    
    st.header("⚙️ Configuración de Round Robin")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        quantum = st.slider(
            "Tamaño del Quantum (ticks)",
            min_value=1,
            max_value=10,
            value=st.session_state.config_rr['quantum'],
            help="Tiempo máximo que un proceso puede ejecutar antes de ser interrumpido"
        )
        st.session_state.config_rr['quantum'] = quantum
    
    with col2:
        usar_cc = st.checkbox(
            "Usar cambio de contexto",
            value=st.session_state.config_rr['usar_cambio_contexto'],
            help="Simular el overhead del cambio entre procesos"
        )
        if usar_cc and st.session_state.config_rr['cambio_contexto'] == 0:
            st.session_state.config_rr['cambio_contexto'] = 1
        
        st.session_state.config_rr['usar_cambio_contexto'] = usar_cc
    
    with col3:
        if usar_cc:
            current_value = st.session_state.config_rr['cambio_contexto']
            if current_value < 1:
                current_value = 1
                st.session_state.config_rr['cambio_contexto'] = current_value
            
            cc_duracion = st.number_input(
                "Duración cambio contexto (ticks)",
                min_value=1,
                max_value=5,
                value=current_value,  
                help="Tiempo que toma cambiar entre procesos",
                key="cc_input_active"
            )
            st.session_state.config_rr['cambio_contexto'] = cc_duracion
        else:
            st.text_input(
                "Duración cambio contexto",
                value="Desactivado",
                disabled=True,
                help="Activa 'Usar cambio de contexto' para habilitar",
                key="cc_placeholder_disabled"
            )
    
    st.info(f"""
    **Configuración actual:**
    - **Quantum:** {st.session_state.config_rr['quantum']} ticks
    - **Cambio de contexto:** {'Activado (' + str(st.session_state.config_rr['cambio_contexto']) + ' ticks)' if st.session_state.config_rr['usar_cambio_contexto'] else 'Desactivado'}
    - **Procesos en espera:** {len(st.session_state.procesos_rr) if st.session_state.procesos_rr else 0}
    """)
    
    st.header("📥 Configuración de Procesos")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        num_procesos = st.number_input(
            "Número de procesos",
            min_value=1,
            max_value=8,
            value=4,
            key="rr_procesos"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔄 Reiniciar Procesos", use_container_width=True):
            st.session_state.procesos_rr = []
            st.session_state.simulacion_iniciada_rr = False
            st.rerun()
    
    st.subheader("✏️ Definir Procesos Round Robin")
    
    if not st.session_state.procesos_rr:
        st.session_state.procesos_rr = [
            {'pid': i, 'llegada': 0, 'duracion': (i+1)*2} 
            for i in range(num_procesos)
        ]
    
    procesos_rr = []
    for i in range(num_procesos):
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.write(f"**Proceso {i}**")
        with col2:
            llegada = st.number_input(
                f"Llegada P{i}",
                min_value=0,
                value=st.session_state.procesos_rr[i]['llegada'] if i < len(st.session_state.procesos_rr) else 0,
                key=f"llegada_rr_{i}"
            )
        with col3:
            duracion = st.number_input(
                f"Duración P{i}",
                min_value=1,
                value=st.session_state.procesos_rr[i]['duracion'] if i < len(st.session_state.procesos_rr) else (i+1)*2,
                key=f"duracion_rr_{i}"
            )
        
        procesos_rr.append({
            'pid': i,
            'llegada': llegada,
            'duracion': duracion
        })
    
    st.session_state.procesos_rr = procesos_rr
    
    if st.session_state.procesos_rr:
        st.subheader("📋 Procesos Configurados")
        df_procesos = pd.DataFrame(st.session_state.procesos_rr)
        df_procesos['Proceso'] = df_procesos['pid'].apply(lambda x: f'P{x}')
        st.dataframe(df_procesos[['Proceso', 'llegada', 'duracion']], use_container_width=True)
    
    st.header("🎯 Simulación Round Robin")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🚀 Ejecutar Simulación RR", type="primary", use_container_width=True):
            es_valido, mensaje = validar_procesos(st.session_state.procesos_rr)
            if es_valido:
                with st.spinner("Ejecutando Round Robin..."):
                    cambio_contexto = st.session_state.config_rr['cambio_contexto'] if st.session_state.config_rr['usar_cambio_contexto'] else 0
                    
                    procesos_calculados = calcular_rr(
                        st.session_state.procesos_rr.copy(),
                        quantum=st.session_state.config_rr['quantum'],
                        cambio_contexto=cambio_contexto
                    )
                    
                    st.session_state.procesos_calculados_rr = procesos_calculados
                    st.session_state.tiempo_actual_rr = 0
                    st.session_state.simulacion_iniciada_rr = True
                    st.rerun()
            else:
                st.error(f"❌ {mensaje}")
    
    with col2:
        if st.button("🔄 Reiniciar Simulación", use_container_width=True):
            st.session_state.simulacion_iniciada_rr = False
            st.session_state.tiempo_actual_rr = 0
            st.rerun()
    
    if st.session_state.get("simulacion_iniciada_rr", False):
        st.header("📊 Resultados de la Simulación Round Robin")
        
        tiempo_actual = st.session_state.tiempo_actual_rr
        tiempo_total = calcular_tiempo_total(st.session_state.procesos_calculados_rr)
        
        st.subheader(f"⏰ Tiempo Actual: {tiempo_actual} / {tiempo_total}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⏮️ Reiniciar", key="reiniciar_rr", use_container_width=True):
                st.session_state.tiempo_actual_rr = 0
                st.rerun()
        
        with col2:
            if st.button("◀️ Retroceder", key="retroceder_rr", use_container_width=True):
                if st.session_state.tiempo_actual_rr > 0:
                    st.session_state.tiempo_actual_rr -= 1
                    st.rerun()
        
        with col3:
            if st.button("Avanzar ▶️", key="avanzar_rr", use_container_width=True):
                if st.session_state.tiempo_actual_rr < tiempo_total:
                    st.session_state.tiempo_actual_rr += 1
                    st.rerun()
        
        with col4:
            if st.button("▶️▶️ Ver Todo", key="vertodo_rr", use_container_width=True):
                st.session_state.tiempo_actual_rr = tiempo_total
                st.rerun()
        
        if tiempo_total > 0:
            st.progress(st.session_state.tiempo_actual_rr / tiempo_total)
        else:
            st.progress(0)
        
        fig = crear_grafico_gantt(
            st.session_state.procesos_calculados_rr,
            st.session_state.tiempo_actual_rr,
            "Round Robin"
        )
        st.pyplot(fig)
        
        if st.session_state.tiempo_actual_rr == tiempo_total:
            st.markdown("---")
            st.subheader("📈 Métricas Finales Round Robin")
            
            metricas = mostrar_metricas(st.session_state.procesos_calculados_rr)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("⏱️ Retorno Promedio", f"{metricas['retorno_promedio']:.2f}")
            with col2:
                st.metric("⏳ Espera Promedio", f"{metricas['espera_promedio']:.2f}")
            with col3:
                st.metric("✅ Procesos Completados", metricas['procesos_completados'])
            with col4:
                st.metric("🔁 Quantum", st.session_state.config_rr['quantum'])
            
            if st.session_state.config_rr['usar_cambio_contexto']:
                total_cambios = sum(len(p.get('ejecuciones', [])) - 1 for p in st.session_state.procesos_calculados_rr if len(p.get('ejecuciones', [])) > 1)
                tiempo_cambios = total_cambios * st.session_state.config_rr['cambio_contexto']
                st.info(f"**Cambios de contexto:** {total_cambios} cambios, {tiempo_cambios} ticks de overhead")
        
        with st.expander("📋 Ver detalles de procesos calculados"):
            st.dataframe(pd.DataFrame(st.session_state.procesos_calculados_rr))
    
    with st.expander("📚 Explicación Detallada del Algoritmo Round Robin"):
        st.markdown("""
        ## 🔄 Round Robin
        
        **¿Cómo funciona?**
        
        Round Robin es un algoritmo preemptivo que:
        
        1. **Asigna un quantum** de tiempo fijo a cada proceso
        2. **Ejecuta cada proceso** por su quantum o hasta que termine
        3. **Si no termina**, vuelve al final de la cola
        4. **Repite** hasta que todos los procesos terminen
        
        **Ejemplo práctico (quantum=4):**
        ```
        Procesos: P0(duración=6), P1(duración=4), P2(duración=8)
        
        Tiempo 0-4: Ejecuta P0 (4/6 completado)
        Tiempo 4-8: Ejecuta P1 (completo - 4/4)
        Tiempo 8-12: Ejecuta P2 (4/8 completado)  
        Tiempo 12-14: Ejecuta P0 (restante 2/6 - completo)
        Tiempo 14-18: Ejecuta P2 (4/8 más - completo)
        ```
        
        **Ventajas:**
        - ✅ **Muy justo** - todos los procesos reciben igual atención
        - ✅ **Excelente para sistemas interactivos** - buen tiempo de respuesta
        - ✅ **Simple de implementar**
        - ✅ **Evita la inanición** - todos progresan
        
        **Desventajas:**
        - ❌ **Rendimiento depende del quantum**
        - ❌ **Quantum muy grande** → similar a FCFS
        - ❌ **Quantum muy pequeño** → mucho overhead
        - ❌ **No óptimo** para minimizar tiempos de espera
        
        **Selección del quantum óptimo:**
        - **Quantum muy grande (>50 ticks):** Similar a FCFS, pobre respuesta
        - **Quantum muy pequeño (<5 ticks):** Mucho overhead por cambios de contexto  
        - **Quantum ideal (10-30 ticks):** Balance entre respuesta y overhead
        
        **Fórmula de throughput:**
        ```
        Throughput ≈ Número de procesos / (Tiempo total + Overhead cambios contexto)
        ```
        
        **Aplicaciones en la vida real:**
        - Sistemas operativos de tiempo compartido
        - Servidores web y aplicaciones
        - Entornos de desarrollo interactivos
        - Cualquier sistema con múltiples usuarios
        
        **Consejo:** El quantum ideal depende de la carga del sistema. 
        En sistemas modernos, típicamente está entre 10-100ms.
        """)

if __name__ == "__main__":
    main()