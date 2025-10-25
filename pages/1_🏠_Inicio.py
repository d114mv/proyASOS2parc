import streamlit as st

st.set_page_config(
    page_title="Inicio - Simulador Planificación",
    page_icon="🏠",
    layout="wide"
)

# Estilos CSS CORREGIDOS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .team-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #3498db;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .algo-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .algo-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .algo-card h3 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .algo-card p {
        color: #555;
        margin-bottom: 0.5rem;
    }
    .algo-card ul {
        color: #555;
        margin-bottom: 0;
    }
    .algo-card li {
        margin-bottom: 0.2rem;
    }
    .step-card {
        text-align: center;
        padding: 1.5rem;
        background: white;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .step-card h4 {
        color: #2c3e50;
        margin: 1rem 0 0.5rem 0;
    }
    .step-card p {
        color: #666;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header principal - CORREGIDO (sin transparencia)
    st.markdown('<div class="main-header">⚙️ Simulador de Planificación de Procesos</div>', unsafe_allow_html=True)
    
    # Introducción
    st.markdown("""
    <div style='text-align: center; font-size: 1.2rem; color: #555; margin-bottom: 3rem;'>
        Plataforma educativa para simular y comprender algoritmos de planificación 
        de procesos en Sistemas Operativos
    </div>
    """, unsafe_allow_html=True)
    
    # Información del equipo - CORREGIDO
    st.markdown("### 👥 Equipo de Desarrollo")
    st.markdown("""
    <div class="team-card">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👨‍💻</div>
                <h4 style="color: #2c3e50; margin: 0.5rem 0;">Muriel Vargas Dilan Itamar</h4>
            </div>
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👨‍💻</div>
                <h4 style="color: #2c3e50; margin: 0.5rem 0;">Quintana Callejas Marco Antonio</h4>
            </div>
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👨‍💻</div>
                <h4 style="color: #2c3e50; margin: 0.5rem 0;">Murillo Rodriguez Juan Rodolfo</h4>
            </div>
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👨‍💻</div>
                <h4 style="color: #2c3e50; margin: 0.5rem 0;">Aduviri Calizaya Leonel</h4>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Algoritmos disponibles - CORREGIDO
    st.markdown("### 🎯 Algoritmos Disponibles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # FCFS
        st.markdown("""
        <div class="algo-card">
            <h3>⚙️ FCFS</h3>
            <p><strong>First Come First Served</strong></p>
            <p>Planificación por orden de llegada - El primero en llegar es el primero en ser servido</p>
            <ul>
                <li>✅ Simple de implementar</li>
                <li>❌ Efecto convoy (procesos largos retrasan cortos)</li>
                <li>⏱️ No preemptivo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # SJF
        st.markdown("""
        <div class="algo-card">
            <h3>📊 SJF</h3>
            <p><strong>Shortest Job First</strong></p>
            <p>Ejecuta primero los procesos con menor tiempo de CPU requerido</p>
            <ul>
                <li>✅ Minimiza tiempo de espera promedio</li>
                <li>❌ Inanición para procesos largos</li>
                <li>⏱️ No preemptivo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # SRT
        st.markdown("""
        <div class="algo-card">
            <h3>⚡ SRT</h3>
            <p><strong>Shortest Remaining Time</strong></p>
            <p>Versión preemptiva de SJF - Siempre ejecuta el proceso con menor tiempo restante</p>
            <ul>
                <li>✅ Excelente tiempo de respuesta</li>
                <li>❌ Overhead por cambios de contexto</li>
                <li>⏱️ Preemptivo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Round Robin
        st.markdown("""
        <div class="algo-card">
            <h3>🔄 Round Robin</h3>
            <p><strong>Planificación con Quantum</strong></p>
            <p>Asigna intervalos de tiempo fijos (quantum) a cada proceso</p>
            <ul>
                <li>✅ Justo para todos los procesos</li>
                <li>❌ Rendimiento depende del quantum</li>
                <li>⏱️ Preemptivo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Prioridad
        st.markdown("""
        <div class="algo-card">
            <h3>🎯 Prioridad</h3>
            <p><strong>Planificación por Niveles</strong></p>
            <p>Ejecuta procesos basado en niveles de prioridad asignados</p>
            <ul>
                <li>✅ Flexible para diferentes necesidades</li>
                <li>❌ Inanición para prioridades bajas</li>
                <li>⏱️ Puede ser preemptivo o no</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Cómo usar - CORREGIDO
    st.markdown("---")
    st.markdown("### 📖 Cómo Usar el Simulador")
    
    steps_col1, steps_col2, steps_col3 = st.columns(3)
    
    with steps_col1:
        st.markdown("""
        <div class="step-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">1️⃣</div>
            <h4>Selecciona un Algoritmo</h4>
            <p>Elige entre los 5 algoritmos disponibles según tus necesidades de estudio</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col2:
        st.markdown("""
        <div class="step-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">2️⃣</div>
            <h4>Configura los Procesos</h4>
            <p>Define los tiempos de llegada, duración y prioridades de cada proceso</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col3:
        st.markdown("""
        <div class="step-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">3️⃣</div>
            <h4>Analiza Resultados</h4>
            <p>Observa la ejecución en tiempo real y métricas de desempeño</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Métricas explicadas
    with st.expander("📊 Métricas que Calculamos"):
        st.markdown("""
        **⏱️ Tiempo de Retorno (Turnaround Time):**
        - Tiempo total desde la llegada hasta la finalización
        - *Fórmula: Tiempo Final - Tiempo de Llegada*
        
        **⏳ Tiempo de Espera (Waiting Time):**
        - Tiempo que el proceso pasa esperando en la cola de listos
        - *Fórmula: Tiempo de Retorno - Tiempo de CPU*
        
        **🚀 Throughput:**
        - Número de procesos completados por unidad de tiempo
        - *Fórmula: Procesos Completados / Tiempo Total*
        
        **⚡ Tiempo de Respuesta:**
        - Tiempo desde la llegada hasta la primera ejecución (solo algoritmos preemptivos)
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>Proyecto Académico - Administración de Sistemas Operativos y Servidores - Escuela Militar de Ingeniería U.A. Cochabamba</strong></p>
        <p>Simulador desarrollado para fines educativos y de investigación</p>
        <p>© 2025 - CodeStorm - Todos los derechos reservados.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()