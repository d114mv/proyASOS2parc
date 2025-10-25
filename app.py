import streamlit as st

st.set_page_config(
    page_title="Simulador de Planificación",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados MEJORADOS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    
    /* Botones de algoritmos personalizados */
    .algo-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 2rem 1rem;
        border-radius: 15px;
        font-size: 1.1rem;
        font-weight: 500;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .algo-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .algo-btn-large {
        height: 160px;
        padding: 2.5rem 1rem;
    }
    
    .algo-title {
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .algo-desc {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .algo-subdesc {
        font-size: 0.9rem;
        opacity: 0.8;
        font-style: italic;
        margin-top: 0.3rem;
    }

    .developer-card {
        background: #2e3440;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #88c0d0;
        color: white;
        font-size: 1rem;
    }
    
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .feature-list li {
        margin: 0.8rem 0;
        padding-left: 1.5rem;
        position: relative;
    }
    
    .feature-list li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #88c0d0;
        font-weight: bold;
    }
    
    /* Ocultar el botón nativo de Streamlit */
    .stButton > button {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

def create_algo_button(icon, title, description, subdescription=None, large=False):
    """Crea un botón de algoritmo personalizado"""
    button_class = "algo-btn-large" if large else "algo-btn"
    subdesc_html = f'<div class="algo-subdesc">{subdescription}</div>' if subdescription else ''
    
    html = f'''
    <div class="{button_class}" onclick="this.parentElement.querySelector('button').click()">
        <div class="algo-title">{icon} {title}</div>
        <div class="algo-desc">{description}</div>
        {subdesc_html}
    </div>
    '''
    return html

def main():
    st.markdown('<h1 class="main-header">🧠 Simulador de Algoritmos de Planificación</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🚀 Selecciona un Algoritmo")
        
        # Primera fila de algoritmos
        col_a, col_b = st.columns(2)
        
        with col_a:
            # FCFS
            st.markdown(create_algo_button("⚙️", "FCFS", "First Come First Served"), unsafe_allow_html=True)
            if st.button("Ir a FCFS", key="fcfs", use_container_width=True):
                st.switch_page("pages/2_⚙️_FCFS.py")
            
            # SJF
            st.markdown(create_algo_button("📊", "SJF", "Shortest Job First"), unsafe_allow_html=True)
            if st.button("Ir a SJF", key="sjf", use_container_width=True):
                st.switch_page("pages/3_📊_SJF.py")

            # SRT
            st.markdown(create_algo_button("⚡", "SRT", "Shortest Remaining Time"), unsafe_allow_html=True)
            if st.button("Ir a SRT", key="srt", use_container_width=True):
                st.switch_page("pages/6_⚡_SRT.py")
        
        with col_b:
            # Round Robin
            st.markdown(create_algo_button("🔄", "Round Robin", "Planificación con Quantum"), unsafe_allow_html=True)
            if st.button("Ir a Round Robin", key="rr", use_container_width=True):
                st.switch_page("pages/4_🔄_Round_Robin.py")
            
            # Prioridad
            st.markdown(create_algo_button("🎯", "Prioridad", "Planificación por Niveles"), unsafe_allow_html=True)
            if st.button("Ir a Prioridad", key="pri", use_container_width=True):
                st.switch_page("pages/5_🎯_Prioridad.py")
    
    with col2:
        st.markdown("### 📋 Características del Simulador")
        
        st.markdown("""
        <div class="info-box">
            <h3>🎯 Funcionalidades</h3>
            <ul class="feature-list">
                <li><strong>Entrada interactiva</strong> de procesos</li>
                <li><strong>Visualización en tiempo real</strong></li>
                <li><strong>Métricas de rendimiento</strong></li>
                <li><strong>Diagramas de Gantt interactivos</strong></li>
                <li><strong>Controles de simulación</strong></li>
                <li><strong>Comparativa de algoritmos</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 👥 Desarrollado por:")
        
        developers = [
            "Muriel Vargas Dilan Itamar",
            "Quintana Callejas Marco Antonio", 
            "Murillo Rodriguez Juan Rodolfo",
            "Aduviri Calizaya Leonel"
        ]
        
        for dev in developers:
            st.markdown(f'<div class="developer-card">🧑‍💻 {dev}</div>', unsafe_allow_html=True)
        
        # Información adicional
        with st.expander("ℹ️ Acerca del Proyecto"):
            st.markdown("""
            **Proyecto Académico - Administración de Sistemas Operativos y Servidores - Escuela Militar de Ingeniería U.A. Cochabamba**
            
            Este simulador permite estudiar y comparar diferentes 
            algoritmos de planificación de procesos utilizados 
            en sistemas operativos.
            
            **Tecnologías utilizadas:**
            - Streamlit
            - Matplotlib
            - Pandas
            - NumPy
            
            © 2025 - CodeStorm - Todos los derechos reservados.
            """)

if __name__ == "__main__":
    main()